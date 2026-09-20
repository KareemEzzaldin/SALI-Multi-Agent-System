"""
SALI — Misconception Detection API Route (Step 2)
Exposes endpoints for aggregated error diagnosis, Claude 3.5 Sonnet prompt generation,
and Cognitive Twin state linking.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

from ..models.schemas import Attempt, MisconceptionSignal
from ..models.knowledge_state import ConceptKnowledgeState
from ..engine.misconception_analyzer import (
    HistoryAggregator,
    MisconceptionDiagnosticResult,
    MisconceptionStateLinker,
    build_claude_misconception_prompt
)
from .knowledge_tracing_routes import LEARNER_DB

router = APIRouter(prefix="/api/v1/misconceptions", tags=["Misconception Detection"])


class MisconceptionAnalysisRequest(BaseModel):
    learner_id: str
    concept_id: str
    concept_name: str
    attempts: List[Attempt]
    question_text: str
    correct_answer: str
    learner_answer: str
    is_correct: bool
    course_evidence_text: str


@router.post("/detect", response_model=MisconceptionDiagnosticResult, status_code=status.HTTP_200_OK)
async def detect_and_link_misconception(req: MisconceptionAnalysisRequest):
    """
    1. Aggregates error history across all past attempts.
    2. Builds the Claude 3.5 Sonnet diagnostic prompt.
    3. Formulates the misconception signal.
    4. Links and updates the learner's Cognitive Twin state if found in DB.
    """
    # 1. Aggregate error patterns
    aggregated = HistoryAggregator.aggregate(
        attempts=req.attempts,
        concept_name=req.concept_name,
        current_answer=req.learner_answer,
        is_correct=req.is_correct
    )

    # 2. Build the optimized Claude 3.5 Sonnet prompt
    prompts = build_claude_misconception_prompt(
        aggregated_history=aggregated,
        question_text=req.question_text,
        correct_answer=req.correct_answer,
        learner_answer=req.learner_answer,
        course_evidence_snippet=req.course_evidence_text
    )

    # 3. Formulate diagnosis (Rule-backed baseline + ready for LLM client execution)
    # In production with API key: client.messages.create(model="claude-3-5-sonnet-20241022", ...)
    if not req.is_correct and aggregated.failed_attempts_count >= 1:
        detected = True
        confidence = min(0.60 + 0.15 * aggregated.consecutive_failures, 0.95)
        category = "mental_model_flaw"
        description = (
            f"Persistent confusion detected in '{req.concept_name}'. The learner repeatedly "
            f"misinterprets core mechanics across {aggregated.failed_attempts_count} failed attempts."
        )
    else:
        detected = False
        confidence = 0.0
        category = "none"
        description = "No recurring misconception detected. Error appears transient or answer is correct."

    signal = MisconceptionSignal(
        detected=detected,
        concept_name=req.concept_name,
        misunderstanding_description=description,
        confidence_score=round(confidence, 2)
    )

    # 4. State Linking with the learner's Cognitive Twin
    linked_state: Optional[ConceptKnowledgeState] = None
    if req.learner_id in LEARNER_DB and req.concept_id in LEARNER_DB[req.learner_id]:
        current_state = LEARNER_DB[req.learner_id][req.concept_id]
        updated_state = MisconceptionStateLinker.link_to_cognitive_twin(
            state=current_state,
            misconception=signal,
            category=category
        )
        LEARNER_DB[req.learner_id][req.concept_id] = updated_state
        linked_state = updated_state

    return MisconceptionDiagnosticResult(
        signal=signal,
        category=category,
        linked_state=linked_state
    )


@router.post("/build-prompt")
async def generate_claude_prompt(req: MisconceptionAnalysisRequest):
    """
    Utility endpoint: returns the formatted Claude 3.5 Sonnet XML prompt for inspection or direct dispatch.
    """
    aggregated = HistoryAggregator.aggregate(
        attempts=req.attempts,
        concept_name=req.concept_name,
        current_answer=req.learner_answer,
        is_correct=req.is_correct
    )
    return build_claude_misconception_prompt(
        aggregated_history=aggregated,
        question_text=req.question_text,
        correct_answer=req.correct_answer,
        learner_answer=req.learner_answer,
        course_evidence_snippet=req.course_evidence_text
    )
