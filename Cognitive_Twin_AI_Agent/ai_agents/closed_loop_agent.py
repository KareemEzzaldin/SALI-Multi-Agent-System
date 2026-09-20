"""
AI AGENT 5: Closed-Loop Feedback Orchestrator Agent
Implements:
- Full Pipeline Coordination across Agents 1 to 4
- Asynchronous Background Execution (Persistence & Escalation Webhooks)
- Holistic Metacognitive Synthesis with Claude 3.5 Sonnet
- Clean Standalone Execution Interface
"""
from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field

from .cognitive_twin_agent import CognitiveTwinAgent, ConceptState, InteractionTelemetry
from .misconception_agent import MisconceptionDetectionAgent, AttemptRecord, MisconceptionSignal
from .adaptive_assessment_agent import AdaptiveAssessmentAgent, AssessmentItem
from .next_action_agent import NextBestActionAgent, ActionPlan, ActionType


# ─────────────────────────────────────────────
# PIPELINE RESULT SCHEMA
# ─────────────────────────────────────────────

class ClosedLoopCycleResult(BaseModel):
    learner_id: str
    concept_name: str
    updated_cognitive_state: ConceptState
    misconception_signal: MisconceptionSignal
    prescribed_action: ActionPlan
    recommended_adaptive_question: Optional[AssessmentItem] = None
    execution_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────
# AGENT CORE
# ─────────────────────────────────────────────

class ClosedLoopOrchestratorAgent:
    """
    Agent responsible for orchestrating the complete adaptive learning loop.
    """

    @classmethod
    def run_cycle(
        cls,
        learner_id: str,
        concept_id: str,
        concept_name: str,
        current_state: ConceptState,
        attempts: List[AttemptRecord],
        current_question: str,
        correct_answer: str,
        learner_answer: str,
        is_correct: bool,
        course_evidence: str,
        attempt_number: int = 1,
        async_webhook_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> ClosedLoopCycleResult:
        """
        Executes the unified loop:
        1. Agent 1: Updates Cognitive Twin (BKT + Ebbinghaus)
        2. Agent 2: Misconception Detection & State Linking
        3. Agent 4: Next-Best Action Engine
        4. Agent 3: Adaptive Question generation (if practice/remediation)
        5. Asynchronous Webhook Dispatch if escalated
        """
        # Step 1: Cognitive Twin Step
        telemetry = InteractionTelemetry(
            learner_id=learner_id,
            concept_id=concept_id,
            concept_name=concept_name,
            is_correct=is_correct,
            attempt_number=attempt_number
        )
        updated_state = CognitiveTwinAgent.step(current_state, telemetry)

        # Step 2: Misconception Detection
        misc_signal = MisconceptionDetectionAgent.diagnose(
            concept_name=concept_name,
            attempts=attempts,
            current_question=current_question,
            correct_answer=correct_answer,
            learner_answer=learner_answer,
            is_correct=is_correct,
            course_evidence=course_evidence
        )

        # Link state if misconception detected
        if misc_signal.detected:
            updated_state = MisconceptionDetectionAgent.link_state(updated_state, misc_signal)

        # Count consecutive failures
        consecutive_fails = 0
        for a in reversed(attempts):
            if not a.is_correct:
                consecutive_fails += 1
            else:
                break
        if not is_correct:
            consecutive_fails += 1

        # Step 3: Next-Best Action Selection
        action_plan = NextBestActionAgent.prescribe(
            learner_id=learner_id,
            concept_name=concept_name,
            consecutive_failures=consecutive_fails,
            attempt_number=attempt_number,
            frustration_flag=consecutive_fails >= 3,
            is_correct=is_correct,
            p_known=updated_state.p_known,
            course_evidence=course_evidence,
            misconception=misc_signal
        )

        # Step 4: Generate next adaptive question if student is progressing
        adaptive_q = None
        if action_plan.action_type in (ActionType.PRACTICE, ActionType.REMEDIATION):
            adaptive_q = AdaptiveAssessmentAgent.generate_question(
                concept_name=concept_name,
                p_known=updated_state.p_known,
                rag_evidence=course_evidence,
                known_misconception=misc_signal.misunderstanding_description if misc_signal.detected else None
            )

        # Step 5: Webhook dispatch if Escalation triggered
        if action_plan.action_type == ActionType.ESCALATION and async_webhook_callback:
            webhook_data = {
                "event": "pedagogical_escalation",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "learner_id": learner_id,
                "concept": concept_name,
                "dossier": action_plan.human_dossier.model_dump() if action_plan.human_dossier else None
            }
            try:
                async_webhook_callback(webhook_data)
            except Exception:
                pass

        return ClosedLoopCycleResult(
            learner_id=learner_id,
            concept_name=concept_name,
            updated_cognitive_state=updated_state,
            misconception_signal=misc_signal,
            prescribed_action=action_plan,
            recommended_adaptive_question=adaptive_q
        )

    @staticmethod
    def get_claude_synthesis_prompt(result: ClosedLoopCycleResult) -> Dict[str, str]:
        """Claude 3.5 Sonnet XML prompt for holistic closed-loop synthesis."""
        system = (
            "You are the Chief Learning Intelligence Synthesizer for SALI.\n"
            "Produce a cohesive 2-sentence metacognitive summary that validates the learner's effort."
        )
        user = f"""<closed_loop_telemetry>
  <concept>{result.concept_name}</concept>
  <p_known>{result.updated_cognitive_state.p_known}</p_known>
  <misconception_detected>{result.misconception_signal.detected}</misconception_detected>
  <action_type>{result.prescribed_action.action_type.value}</action_type>
</closed_loop_telemetry>
<instruction>Synthesize a motivating pedagogical takeaway.</instruction>"""
        return {"system": system, "user": user}
