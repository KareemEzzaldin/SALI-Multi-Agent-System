"""
SALI — Pydantic Schemas
Defines all input and output data structures for the AI Engine.
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# INPUT SCHEMAS
# ─────────────────────────────────────────────

class Attempt(BaseModel):
    attempt_number: int
    question_id: str
    question_text: str
    correct_answer: str
    learner_answer: str
    is_correct: bool
    timestamp: str  # ISO-8601


class ConceptMastery(BaseModel):
    concept_name: str
    mastery_score: float = Field(..., ge=0.0, le=1.0)
    last_practiced: str  # ISO-8601 date string


class LearnerHistory(BaseModel):
    learner_id: str
    learner_name: str
    attempts: List[Attempt]
    mastery_vector: List[ConceptMastery]


class CurrentInteraction(BaseModel):
    question_id: str
    question_text: str
    correct_answer: str
    learner_answer: str
    is_correct: bool


class CourseEvidence(BaseModel):
    concept_name: str
    source_text: str  # The RAG-retrieved passage that grounds remediation


class AnalyzeRequest(BaseModel):
    learner_history: LearnerHistory
    current_interaction: CurrentInteraction
    course_evidence: CourseEvidence


# ─────────────────────────────────────────────
# OUTPUT SCHEMAS (matches spec exactly)
# ─────────────────────────────────────────────

class MisconceptionSignal(BaseModel):
    detected: bool
    concept_name: str
    misunderstanding_description: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class LearnerStateUpdate(BaseModel):
    target_concept: str
    mastery_delta: float = Field(..., ge=-1.0, le=1.0)
    forgetting_risk_adjustment: float


class ActionType(str, Enum):
    socratic_tutoring = "socratic_tutoring"
    remediation = "remediation"
    practice = "practice"
    escalation = "escalation"


class NextAction(BaseModel):
    action_type: ActionType
    reasoning: str
    generated_response_or_question: str


class AnalyzeResponse(BaseModel):
    MisconceptionSignal: MisconceptionSignal
    LearnerStateUpdate: LearnerStateUpdate
    NextAction: NextAction
