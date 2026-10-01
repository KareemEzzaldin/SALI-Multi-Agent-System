"""
SALI — Bayesian Knowledge Tracing (BKT) & Ebbinghaus Decay Engine
Optimized for mathematical stability and pedagogical realism.
"""
import math
from datetime import datetime, timezone
from typing import Tuple
from ..models.knowledge_state import BKTParameters, ConceptKnowledgeState, InteractionTelemetry


class KnowledgeTracingEngine:
    @staticmethod
    def calculate_ebbinghaus_retention(last_practiced: datetime, stability_days: float) -> Tuple[float, float]:
        """
        Calculates memory retention R and forgetting risk:
        R = e^(-t / S)
        t: time elapsed in days
        S: memory stability
        """
        now = datetime.now(timezone.utc)
        elapsed_seconds = (now - last_practiced).total_seconds()
        t_days = max(elapsed_seconds / 86400.0, 0.0)

        # Exponential decay
        retention = math.exp(-t_days / max(stability_days, 0.1))
        retention = round(max(min(retention, 1.0), 0.0), 4)
        forgetting_risk = round(1.0 - retention, 4)

        return retention, forgetting_risk

    @staticmethod
    def update_bkt_mastery(
        prior_p_known: float,
        is_correct: bool,
        params: BKTParameters
    ) -> float:
        """
        Standard Bayesian Knowledge Tracing update rule:
        1. Observation Update: P(L_t | Obs)
        2. Transition Step: P(L_{t+1}) = P(L_t | Obs) + (1 - P(L_t | Obs)) * P(Transit)
        """
        p_l = prior_p_known
        p_g = params.p_guess
        p_s = params.p_slip
        p_t = params.p_transit

        # Step 1: Posterior update given evidence
        if is_correct:
            numerator = p_l * (1.0 - p_s)
            denominator = (p_l * (1.0 - p_s)) + ((1.0 - p_l) * p_g)
        else:
            numerator = p_l * p_s
            denominator = (p_l * p_s) + ((1.0 - p_l) * (1.0 - p_g))

        # Numerical safety guard
        p_posterior = numerator / denominator if denominator > 0 else p_l

        # Step 2: Learning transition update
        p_next = p_posterior + (1.0 - p_posterior) * p_t
        return round(min(max(p_next, 0.001), 0.999), 4)

    @staticmethod
    def update_memory_stability(
        current_stability: float,
        is_correct: bool,
        retention_rate: float
    ) -> float:
        """
        Increases memory stability upon successful recall (spaced repetition effect).
        Stability increases more if recall occurs when retention was low (desirable difficulty).
        """
        if is_correct:
            # Multiplier between 1.5x and 3.0x based on how challenging the retrieval was
            growth_factor = 1.5 + (1.0 - retention_rate) * 1.5
            new_stability = current_stability * growth_factor
        else:
            # Memory lapsed: reduce stability towards baseline
            new_stability = max(current_stability * 0.5, 1.0)

        return round(new_stability, 2)

    @classmethod
    def process_interaction(
        cls,
        state: ConceptKnowledgeState,
        telemetry: InteractionTelemetry,
        bkt_params: BKTParameters = BKTParameters()
    ) -> ConceptKnowledgeState:
        """
        Unified pipeline:
        1. Factor in forgetting decay since last interaction.
        2. Execute BKT update based on new telemetry.
        3. Recalculate stability and reset retention timestamp.
        """
        # 1. Decay prior knowledge by retention rate
        current_retention, _ = cls.calculate_ebbinghaus_retention(
            state.last_practiced, state.memory_stability
        )
        effective_prior = state.p_known * (0.8 + 0.2 * current_retention)

        # 2. Update via BKT
        new_p_known = cls.update_bkt_mastery(effective_prior, telemetry.is_correct, bkt_params)

        # 3. Update memory stability
        new_stability = cls.update_memory_stability(
            state.memory_stability, telemetry.is_correct, current_retention
        )

        consecutive = state.consecutive_correct + 1 if telemetry.is_correct else 0

        # Construct updated state
        return ConceptKnowledgeState(
            concept_id=state.concept_id,
            concept_name=state.concept_name,
            p_known=new_p_known,
            memory_stability=new_stability,
            last_practiced=datetime.now(timezone.utc),
            retention_rate=1.0,  # Just practiced
            forgetting_risk=0.0,
            total_attempts=state.total_attempts + 1,
            consecutive_correct=consecutive
        )
