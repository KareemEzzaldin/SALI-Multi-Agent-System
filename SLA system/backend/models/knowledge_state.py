"""
SALI — Knowledge Tracing & Cognitive Twin State Schemas
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class BKTParameters(BaseModel):
    """Bayesian Knowledge Tracing standard parameters per concept."""
    p_init: float = Field(0.10, ge=0.0, le=1.0, description="P(L0): Prior knowledge probability")
    p_transit: float = Field(0.15, ge=0.0, le=1.0, description="P(T): Probability of learning transition")
    p_guess: float = Field(0.20, ge=0.0, le=1.0, description="P(G): Probability of lucky guess")
    p_slip: float = Field(0.10, ge=0.0, le=1.0, description="P(S): Probability of accidental slip")


class ConceptKnowledgeState(BaseModel):
    """Dynamic Cognitive Twin state for a specific concept."""
    concept_id: str
    concept_name: str
    p_known: float = Field(..., ge=0.0, le=1.0, description="Current BKT probability of mastery P(L)")
    memory_stability: float = Field(1.0, ge=0.1, description="S in Ebbinghaus formula: Halflife in days")
    last_practiced: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retention_rate: float = Field(1.0, ge=0.0, le=1.0, description="R = e^(-t/S)")
    forgetting_risk: float = Field(0.0, ge=0.0, le=1.0, description="1.0 - retention_rate")
    total_attempts: int = Field(0, ge=0)
    consecutive_correct: int = Field(0, ge=0)


class InteractionTelemetry(BaseModel):
    """Telemetry payload received from frontend/client."""
    learner_id: str
    concept_id: str
    concept_name: str
    is_correct: bool
    attempt_number: int = Field(1, ge=1)
    response_time_sec: Optional[float] = Field(None, ge=0.0)
    hints_used: int = Field(0, ge=0)


class CognitiveTwinSnapshot(BaseModel):
    """Full snapshot of the learner's Cognitive Twin across all concepts."""
    learner_id: str
    last_updated: datetime
    concepts: Dict[str, ConceptKnowledgeState]
    overall_mastery_index: float = Field(..., ge=0.0, le=1.0)
