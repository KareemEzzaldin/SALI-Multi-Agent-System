"""
SALI — Next-Best Action Engine Models (Step 4)
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .schemas import ActionType, MisconceptionSignal


class DecisionTelemetry(BaseModel):
    learner_id: str
    concept_id: str
    concept_name: str
    attempt_number: int = Field(1, ge=1)
    consecutive_failures: int = Field(0, ge=0)
    frustration_detected: bool = False
    response_time_sec: Optional[float] = None
    hints_requested: int = Field(0, ge=0)


class HumanEscalationDossier(BaseModel):
    learner_id: str
    concept_name: str
    consecutive_failures: int
    diagnosed_block: str
    suggested_human_intervention: str
    session_urgency: str = Field("medium", description="'low' | 'medium' | 'high'")


class NextActionEvaluation(BaseModel):
    action_type: ActionType
    reasoning: str
    generated_content: str
    follow_up_recommendation: str
    human_dossier: Optional[HumanEscalationDossier] = None


class NextActionDecisionRequest(BaseModel):
    telemetry: DecisionTelemetry
    is_correct: bool
    current_question_text: str
    learner_answer: str
    course_evidence_text: str
    misconception_signal: Optional[MisconceptionSignal] = None
    override_p_known: Optional[float] = Field(None, ge=0.0, le=1.0)
