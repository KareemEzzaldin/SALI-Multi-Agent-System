"""
SALI — Adaptive Assessment Data Schemas (Step 3)
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class DifficultyLevel(str, Enum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class BloomLevel(str, Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"


class QuestionOption(BaseModel):
    key: str = Field(..., description="Option label, e.g., 'A', 'B', 'C', 'D'")
    text: str
    is_misconception_trap: bool = False
    trap_explanation: Optional[str] = None


class AssessmentItem(BaseModel):
    question_id: str
    target_concept: str
    difficulty: DifficultyLevel
    bloom_level: BloomLevel
    question_text: str
    code_snippet: Optional[str] = None
    options: List[QuestionOption]
    correct_option_key: str
    pedagogical_explanation: str
    rag_grounding_quote: str


class GenerateAssessmentRequest(BaseModel):
    learner_id: str
    concept_id: str
    concept_name: str
    rag_course_evidence: str
    known_misconception: Optional[str] = None
    override_difficulty: Optional[DifficultyLevel] = None
