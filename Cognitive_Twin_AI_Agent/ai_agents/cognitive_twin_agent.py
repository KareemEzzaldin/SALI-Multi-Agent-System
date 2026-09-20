"""
AI AGENT 1: Cognitive Twin & Knowledge Tracing Agent
Implements:
- Bayesian Knowledge Tracing (BKT)
- Ebbinghaus Forgetting Risk (R = e^(-t/S))
- Memory Stability Growth Engine
- Claude 3.5 Sonnet Cognitive State Synthesis Prompt
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────

class BKTParameters(BaseModel):
    p_init: float = Field(0.10, ge=0.0, le=1.0, description="P(L0): Prior knowledge probability")
    p_transit: float = Field(0.15, ge=0.0, le=1.0, description="P(T): Probability of learning transition")
    p_guess: float = Field(0.20, ge=0.0, le=1.0, description="P(G): Probability of lucky guess")
    p_slip: float = Field(0.10, ge=0.0, le=1.0, description="P(S): Probability of accidental slip")


class ConceptState(BaseModel):
    concept_id: str
    concept_name: str
    p_known: float = Field(0.10, ge=0.0, le=1.0, description="BKT Probability of mastery P(L)")
    memory_stability: float = Field(1.0, ge=0.1, description="Half-life in days (S)")
    last_practiced: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retention_rate: float = Field(1.0, ge=0.0, le=1.0, description="R = e^(-t/S)")
    forgetting_risk: float = Field(0.0, ge=0.0, le=1.0, description="1.0 - retention_rate")
    total_attempts: int = Field(0, ge=0)
    consecutive_correct: int = Field(0, ge=0)


class InteractionTelemetry(BaseModel):
    learner_id: str
    concept_id: str
    concept_name: str
    is_correct: bool
    attempt_number: int = Field(1, ge=1)
    response_time_sec: Optional[float] = None


# ─────────────────────────────────────────────
# AGENT CORE
# ─────────────────────────────────────────────

class CognitiveTwinAgent:
    """
    Agent responsible for modeling and maintaining the learner's digital knowledge twin.
    """

    @staticmethod
    def calculate_ebbinghaus_decay(last_practiced: datetime, stability_days: float) -> Tuple[float, float]:
        """Calculates current retention rate R and forgetting risk."""
        now = datetime.now(timezone.utc)
        elapsed_days = max((now - last_practiced).total_seconds() / 86400.0, 0.0)
        retention = round(math.exp(-elapsed_days / max(stability_days, 0.1)), 4)
        forgetting_risk = round(1.0 - retention, 4)
        return retention, forgetting_risk

    @staticmethod
    def update_bkt(prior_p_known: float, is_correct: bool, params: BKTParameters) -> float:
        """Standard Bayesian Knowledge Tracing update formula."""
        p_l = prior_p_known
        p_g = params.p_guess
        p_s = params.p_slip
        p_t = params.p_transit

        if is_correct:
            numerator = p_l * (1.0 - p_s)
            denominator = (p_l * (1.0 - p_s)) + ((1.0 - p_l) * p_g)
        else:
            numerator = p_l * p_s
            denominator = (p_l * p_s) + ((1.0 - p_l) * (1.0 - p_g))

        posterior = numerator / denominator if denominator > 0 else p_l
        p_next = posterior + (1.0 - posterior) * p_t
        return round(min(max(p_next, 0.001), 0.999), 4)

    @classmethod
    def step(
        cls,
        current_state: ConceptState,
        telemetry: InteractionTelemetry,
        params: BKTParameters = BKTParameters()
    ) -> ConceptState:
        """Advances the cognitive twin state by one interaction step."""
        current_retention, _ = cls.calculate_ebbinghaus_decay(
            current_state.last_practiced, current_state.memory_stability
        )
        effective_prior = current_state.p_known * (0.8 + 0.2 * current_retention)

        new_p_known = cls.update_bkt(effective_prior, telemetry.is_correct, params)

        if telemetry.is_correct:
            growth = 1.5 + (1.0 - current_retention) * 1.5
            new_stability = round(current_state.memory_stability * growth, 2)
            consecutive = current_state.consecutive_correct + 1
        else:
            new_stability = round(max(current_state.memory_stability * 0.5, 1.0), 2)
            consecutive = 0

        return ConceptState(
            concept_id=current_state.concept_id,
            concept_name=current_state.concept_name,
            p_known=new_p_known,
            memory_stability=new_stability,
            last_practiced=datetime.now(timezone.utc),
            retention_rate=1.0,
            forgetting_risk=0.0,
            total_attempts=current_state.total_attempts + 1,
            consecutive_correct=consecutive
        )

    @staticmethod
    def get_claude_diagnosis_prompt(state: ConceptState, telemetry: InteractionTelemetry) -> Dict[str, str]:
        """Claude 3.5 Sonnet XML diagnostic prompt."""
        system = (
            "You are the Cognitive State Synthesis Engine for SALI.\n"
            "Analyze the learner's empirical knowledge tracing parameters and provide a diagnostic evaluation."
        )
        user = f"""<learner_telemetry>
  <concept>{state.concept_name}</concept>
  <p_known>{state.p_known}</p_known>
  <memory_stability_days>{state.memory_stability}</memory_stability_days>
  <last_interaction correct="{telemetry.is_correct}" attempt="{telemetry.attempt_number}" />
</learner_telemetry>
<instruction>Output JSON diagnosing cognitive stability and review recommendation.</instruction>"""
        return {"system": system, "user": user}
