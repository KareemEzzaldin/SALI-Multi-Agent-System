"""
SALI — Closed-Loop Pipeline Engine (Step 5)
Orchestrates the complete closed-loop feedback cycle:
1. Ingests interaction telemetry and course grounding.
2. Updates Cognitive Twin with Bayesian Knowledge Tracing & Ebbinghaus decay.
3. Performs Misconception Analysis & links state.
4. Triggers Next-Best Action decision engine.
5. Manages asynchronous BackgroundTasks (Persistence & Instructor Escalation Webhooks).
"""
from __future__ import annotations
import logging
from datetime import datetime, timezone, date
from typing import Dict, Any, Optional
from pydantic import BaseModel

from ..models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    MisconceptionSignal,
    LearnerStateUpdate,
    NextAction,
    ActionType
)
from ..models.knowledge_state import (
    ConceptKnowledgeState,
    InteractionTelemetry
)
from ..models.next_action_models import (
    DecisionTelemetry,
    NextActionDecisionRequest
)
from ..engine.knowledge_tracing import KnowledgeTracingEngine
from ..engine.misconception_analyzer import (
    HistoryAggregator,
    MisconceptionStateLinker
)
from ..engine.misconception import detect_misconception
from ..engine.cognitive_twin import compute_cognitive_twin_update
from ..engine.next_action_engine import NextActionEngine
from ..api.knowledge_tracing_routes import LEARNER_DB

logger = logging.getLogger("sali.closed_loop")


# ─────────────────────────────────────────────
# BACKGROUND TASKS & WEBHOOKS
# ─────────────────────────────────────────────

async def async_persist_state(learner_id: str, state_vector: list, save_fn):
    """
    Non-blocking background persistence task.
    Saves the updated Cognitive Twin state to disk/DB.
    """
    try:
        save_fn(learner_id, state_vector)
        logger.info(f"Successfully persisted state for learner '{learner_id}' in background.")
    except Exception as e:
        logger.error(f"Failed to persist state for learner '{learner_id}': {e}")


async def async_dispatch_escalation_webhook(
    learner_id: str,
    concept_name: str,
    dossier: Dict[str, Any]
):
    """
    Dispatches an asynchronous webhook notification when Escalation is triggered.
    Simulates integration with LMS / Slack / Email alert queues.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    webhook_payload = {
        "event": "pedagogical_escalation_triggered",
        "timestamp": timestamp,
        "learner_id": learner_id,
        "concept_name": concept_name,
        "dossier": dossier,
    }
    logger.warning(
        f"🚨 [ESCALATION WEBHOOK DISPATCHED] Learner: {learner_id} | Concept: {concept_name} | Payload: {webhook_payload}"
    )


# ─────────────────────────────────────────────
# CLAUDE 3.5 SONNET HOLISTIC SYNTHESIS PROMPT
# ─────────────────────────────────────────────

def build_claude_closed_loop_synthesis_prompt(
    learner_name: str,
    concept_name: str,
    prior_mastery: float,
    updated_mastery: float,
    misconception_signal: MisconceptionSignal,
    next_action: NextAction
) -> Dict[str, str]:
    """
    Claude 3.5 Sonnet XML prompt for holistic closed-loop reflection.
    """
    system_prompt = (
        "You are the Chief Learning Intelligence Synthesizer for SALI.\n"
        "Your role is to produce a cohesive, metacognitive learning debrief that ties together:\n"
        "1. The learner's updated mastery trajectory.\n"
        "2. The root misconception (if any).\n"
        "3. The recommended adaptive next step.\n\n"
        "Guidelines:\n"
        "- Emphasize growth mindset.\n"
        "- Keep the reflection crisp, encouraging, and pedagogically transparent."
    )

    user_prompt = f"""<closed_loop_session_telemetry>
  <learner>{learner_name}</learner>
  <concept>{concept_name}</concept>
  <trajectory prior_mastery="{prior_mastery:.2f}" updated_mastery="{updated_mastery:.2f}" />
  <misconception detected="{misconception_signal.detected}" confidence="{misconception_signal.confidence_score}">
    {misconception_signal.misunderstanding_description}
  </misconception>
  <prescribed_action type="{next_action.action_type.value}">
    <reasoning>{next_action.reasoning}</reasoning>
  </prescribed_action>
</closed_loop_session_telemetry>

<instruction>
Synthesize this into a 2-sentence metacognitive summary that validates the learner's effort and frames the next action.
</instruction>"""

    return {"system": system_prompt, "user": user_prompt}


# ─────────────────────────────────────────────
# CLOSED-LOOP PIPELINE ORCHESTRATOR
# ─────────────────────────────────────────────

class ClosedLoopPipeline:
    @classmethod
    def execute(
        cls,
        request: AnalyzeRequest,
        persisted_state_loader,
        persisted_state_saver,
        background_tasks
    ) -> AnalyzeResponse:
        """
        Executes the end-to-end closed loop across all 5 roadmap milestones.
        """
        learner = request.learner_history
        current = request.current_interaction
        evidence = request.course_evidence
        concept = evidence.concept_name

        # 1. Load prior state
        persisted = persisted_state_loader(learner.learner_id)
        if persisted:
            try:
                from ..models.schemas import ConceptMastery
                learner.mastery_vector = [ConceptMastery(**item) for item in persisted]
            except Exception:
                pass

        # 2. Extract current mastery
        entry = next(
            (c for c in learner.mastery_vector if c.concept_name.lower() == concept.lower()),
            None,
        )
        current_mastery = entry.mastery_score if entry else 0.10

        prev_attempts_count = sum(1 for a in learner.attempts if a.question_id == current.question_id)
        attempt_number = prev_attempts_count + 1

        consecutive_fails = 0
        for a in reversed(learner.attempts):
            if not a.is_correct:
                consecutive_fails += 1
            else:
                break
        if not current.is_correct:
            consecutive_fails += 1

        # 3. Step 2: Misconception Detection
        misconception = detect_misconception(
            attempts=learner.attempts,
            current_question_id=current.question_id,
            current_answer=current.learner_answer,
            concept_name=concept,
            is_correct=current.is_correct,
        )

        # 4. Step 1: Cognitive Twin State & Forgetting Decay Update
        state_update = compute_cognitive_twin_update(
            mastery_vector=learner.mastery_vector,
            concept_name=concept,
            is_correct=current.is_correct,
            attempt_number=attempt_number,
        )

        # 5. Step 4: Next-Best Action Engine Evaluation
        telemetry = DecisionTelemetry(
            learner_id=learner.learner_id,
            concept_id=f"c_{concept.lower().replace(' ', '_')}",
            concept_name=concept,
            attempt_number=attempt_number,
            consecutive_failures=consecutive_fails,
            frustration_detected=consecutive_fails >= 3
        )
        decision_req = NextActionDecisionRequest(
            telemetry=telemetry,
            is_correct=current.is_correct,
            current_question_text=current.question_text,
            learner_answer=current.learner_answer,
            course_evidence_text=evidence.source_text,
            misconception_signal=misconception,
            override_p_known=current_mastery + state_update.mastery_delta
        )
        action_eval = NextActionEngine.execute_decision_pipeline(
            req=decision_req,
            p_known=max(0.0, min(1.0, current_mastery + state_update.mastery_delta))
        )

        next_action = NextAction(
            action_type=action_eval.action_type,
            reasoning=action_eval.reasoning,
            generated_response_or_question=action_eval.generated_content
        )

        # 6. Step 5: Schedule Non-Blocking Background Tasks (Persistence & Webhooks)
        updated_vector = []
        concept_found = False
        for e in learner.mastery_vector:
            if e.concept_name.lower() == concept.lower():
                new_score = round(max(0.0, min(1.0, e.mastery_score + state_update.mastery_delta)), 4)
                updated_vector.append({
                    "concept_name": e.concept_name,
                    "mastery_score": new_score,
                    "last_practiced": date.today().isoformat(),
                })
                concept_found = True
            else:
                updated_vector.append({
                    "concept_name": e.concept_name,
                    "mastery_score": e.mastery_score,
                    "last_practiced": e.last_practiced,
                })
        if not concept_found:
            new_score = round(max(0.0, min(1.0, state_update.mastery_delta)), 4)
            updated_vector.append({
                "concept_name": concept,
                "mastery_score": new_score,
                "last_practiced": date.today().isoformat(),
            })

        # Background persistence
        background_tasks.add_task(
            async_persist_state,
            learner.learner_id,
            updated_vector,
            persisted_state_saver
        )

        # Background webhook if escalation occurs
        if action_eval.action_type == ActionType.escalation and action_eval.human_dossier:
            background_tasks.add_task(
                async_dispatch_escalation_webhook,
                learner.learner_id,
                concept,
                action_eval.human_dossier.model_dump()
            )

        # 7. Return strictly-typed structured JSON matching original spec
        return AnalyzeResponse(
            MisconceptionSignal=misconception,
            LearnerStateUpdate=state_update,
            NextAction=next_action
        )
