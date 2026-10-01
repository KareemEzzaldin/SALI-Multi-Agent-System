"""
SALI — Next-Best Action API Route (Step 4)
Exposes endpoints for pedagogical decision rule evaluation and Claude 3.5 Sonnet tutor prompt generation.
"""
from fastapi import APIRouter, HTTPException, status
from ..models.next_action_models import (
    NextActionDecisionRequest,
    NextActionEvaluation
)
from ..engine.next_action_engine import NextActionEngine
from .knowledge_tracing_routes import LEARNER_DB

router = APIRouter(prefix="/api/v1/next-action", tags=["Next-Best Action"])


@router.post("/decide", response_model=NextActionEvaluation, status_code=status.HTTP_200_OK)
async def evaluate_next_action(req: NextActionDecisionRequest):
    """
    1. Reads the learner's current mastery from the Cognitive Twin (LEARNER_DB).
    2. Evaluates the multi-criteria decision tree (Escalation / Remediation / Socratic / Practice).
    3. Produces grounded content and an instructor escalation dossier if necessary.
    """
    p_known = req.override_p_known or 0.10
    lid = req.telemetry.learner_id
    cid = req.telemetry.concept_id

    if lid in LEARNER_DB and cid in LEARNER_DB[lid]:
        p_known = LEARNER_DB[lid][cid].p_known

    evaluation = NextActionEngine.execute_decision_pipeline(req=req, p_known=p_known)
    return evaluation


@router.post("/build-tutor-prompt")
async def generate_claude_tutor_prompt(req: NextActionDecisionRequest):
    """
    Utility endpoint: returns the exact Claude 3.5 Sonnet XML prompt for the determined pedagogical mode.
    """
    p_known = req.override_p_known or 0.10
    lid = req.telemetry.learner_id
    cid = req.telemetry.concept_id

    if lid in LEARNER_DB and cid in LEARNER_DB[lid]:
        p_known = LEARNER_DB[lid][cid].p_known

    action, _ = NextActionEngine.evaluate_decision_rules(
        telemetry=req.telemetry,
        is_correct=req.is_correct,
        p_known=p_known,
        misconception=req.misconception_signal
    )

    return NextActionEngine.build_claude_tutor_prompt(
        action_type=action,
        concept_name=req.telemetry.concept_name,
        question_text=req.current_question_text,
        learner_answer=req.learner_answer,
        course_evidence=req.course_evidence_text,
        misconception=req.misconception_signal
    )
