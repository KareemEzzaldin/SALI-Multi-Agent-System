"""
SALI — Adaptive Assessment API Route (Step 3)
Exposes endpoints to generate calibrated assessment items grounded in RAG evidence.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
from ..models.assessment import (
    AssessmentItem,
    GenerateAssessmentRequest,
    DifficultyLevel,
    BloomLevel
)
from ..engine.adaptive_assessment import AdaptiveAssessmentEngine
from .knowledge_tracing_routes import LEARNER_DB

router = APIRouter(prefix="/api/v1/assessment", tags=["Adaptive Assessment"])


@router.post("/generate", response_model=AssessmentItem, status_code=status.HTTP_200_OK)
async def generate_adaptive_question(req: GenerateAssessmentRequest):
    """
    1. Looks up the learner's current mastery P(L) in the Cognitive Twin (LEARNER_DB).
    2. Calibrates optimal difficulty and Bloom's tier (ZPD).
    3. Builds the Claude 3.5 Sonnet prompt with targeted distractor traps.
    4. Produces the structured AssessmentItem grounded in RAG course evidence.
    """
    p_known = 0.10  # default baseline if learner or concept is new
    if req.learner_id in LEARNER_DB and req.concept_id in LEARNER_DB[req.learner_id]:
        p_known = LEARNER_DB[req.learner_id][req.concept_id].p_known

    # 1. Calibrate difficulty or use override
    if req.override_difficulty:
        diff = req.override_difficulty
        bloom = BloomLevel.APPLY if diff == DifficultyLevel.INTERMEDIATE else (
            BloomLevel.ANALYZE if diff == DifficultyLevel.ADVANCED else BloomLevel.UNDERSTAND
        )
    else:
        diff, bloom = AdaptiveAssessmentEngine.calibrate_difficulty(p_known)

    # 2. Build question item (Ready for Claude 3.5 Sonnet API dispatch or deterministic grounded mode)
    item = AdaptiveAssessmentEngine.generate_grounded_fallback(
        concept_name=req.concept_name,
        difficulty=diff,
        bloom_level=bloom,
        rag_evidence=req.rag_course_evidence,
        known_misconception=req.known_misconception
    )

    return item


@router.post("/build-prompt")
async def generate_claude_assessment_prompt(req: GenerateAssessmentRequest):
    """
    Utility endpoint to inspect the Claude 3.5 Sonnet XML prompt for assessment generation.
    """
    p_known = 0.10
    if req.learner_id in LEARNER_DB and req.concept_id in LEARNER_DB[req.learner_id]:
        p_known = LEARNER_DB[req.learner_id][req.concept_id].p_known

    diff = req.override_difficulty or AdaptiveAssessmentEngine.calibrate_difficulty(p_known)[0]
    bloom = BloomLevel.APPLY if diff == DifficultyLevel.INTERMEDIATE else (
        BloomLevel.ANALYZE if diff == DifficultyLevel.ADVANCED else BloomLevel.UNDERSTAND
    )

    return AdaptiveAssessmentEngine.build_claude_assessment_prompt(
        concept_name=req.concept_name,
        difficulty=diff,
        bloom_level=bloom,
        rag_evidence=req.rag_course_evidence,
        known_misconception=req.known_misconception
    )
