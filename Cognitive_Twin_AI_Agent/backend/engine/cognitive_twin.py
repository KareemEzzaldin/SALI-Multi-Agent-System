"""
SALI — Cognitive Twin Engine
Manages learner mastery state with an Ebbinghaus-inspired forgetting curve.
Computes mastery_delta and forgetting_risk_adjustment for each interaction.
"""
from __future__ import annotations
import math
from datetime import date, datetime
from typing import List
from ..models.schemas import ConceptMastery, LearnerStateUpdate


# ─────────────────────────────────────────────
# EBBINGHAUS FORGETTING CURVE
# R = e^(-t / S)
#   t = elapsed days since last practice
#   S = memory stability (higher mastery → higher stability)
# ─────────────────────────────────────────────

def _forgetting_retention(mastery_score: float, days_elapsed: float) -> float:
    """
    Compute retained fraction of memory using Ebbinghaus exponential decay.
    Stability S scales with mastery (stronger understanding → longer retention).
    """
    if days_elapsed <= 0:
        return 1.0
    # Stability: ranges from 1 day (mastery=0) to 30 days (mastery=1)
    stability = 1.0 + 29.0 * mastery_score
    retention = math.exp(-days_elapsed / stability)
    return round(retention, 4)


def _days_since(date_str: str) -> float:
    """Parse an ISO date string and return days elapsed since today."""
    try:
        last_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
    except ValueError:
        last_date = date.fromisoformat(date_str[:10])
    delta = date.today() - last_date
    return max(float(delta.days), 0.0)


def _mastery_delta(
    is_correct: bool,
    attempt_number: int,
    current_mastery: float,
) -> float:
    """
    Compute how much mastery changes given the current interaction result.

    - Correct answer: mastery increases (diminishing returns at high mastery)
    - Wrong answer: mastery decreases slightly (not punished too harshly on first fail)
    - Repeated failures reduce mastery more aggressively
    """
    if is_correct:
        # Learning gain: less gain when mastery is already high
        gain = 0.15 * (1.0 - current_mastery)
        # Bonus for getting it right on first try
        if attempt_number == 1:
            gain *= 1.2
        return round(min(gain, 0.3), 4)
    else:
        # Penalty scales mildly with attempt number to avoid over-penalising
        penalty = 0.08 + 0.04 * min(attempt_number - 1, 4)
        return round(-min(penalty, 0.25), 4)


def compute_cognitive_twin_update(
    mastery_vector: List[ConceptMastery],
    concept_name: str,
    is_correct: bool,
    attempt_number: int,
) -> LearnerStateUpdate:
    """
    Given the learner's current mastery vector and the latest interaction,
    compute the mastery delta and forgetting risk adjustment for the target concept.
    """
    # Find the concept in the mastery vector
    current_mastery_entry = next(
        (c for c in mastery_vector if c.concept_name.lower() == concept_name.lower()),
        None,
    )

    if current_mastery_entry:
        current_mastery = current_mastery_entry.mastery_score
        last_practiced = current_mastery_entry.last_practiced
    else:
        # Brand-new concept — start at zero
        current_mastery = 0.0
        last_practiced = date.today().isoformat()

    # Mastery delta
    delta = _mastery_delta(is_correct, attempt_number, current_mastery)

    # Forgetting risk: how much was forgotten since last practice
    days_elapsed = _days_since(last_practiced)
    retention_before = _forgetting_retention(current_mastery, days_elapsed)
    # Risk = 1 - retention (0 = no risk, 1 = fully forgotten)
    forgetting_risk = round(1.0 - retention_before, 4)

    # Adjustment: practising today resets decay; positive interaction reduces risk
    if is_correct:
        risk_adjustment = -round(forgetting_risk * 0.6, 4)   # risk goes down
    else:
        risk_adjustment = round(forgetting_risk * 0.1, 4)    # small additional risk signal

    return LearnerStateUpdate(
        target_concept=concept_name,
        mastery_delta=delta,
        forgetting_risk_adjustment=risk_adjustment,
    )
