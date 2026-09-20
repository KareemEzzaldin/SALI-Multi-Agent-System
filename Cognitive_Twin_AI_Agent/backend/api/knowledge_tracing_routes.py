"""
SALI — Knowledge Tracing FastAPI Router
Exposes state retrieval and interaction update endpoints.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict
from datetime import datetime, timezone
from ..models.knowledge_state import (
    ConceptKnowledgeState,
    InteractionTelemetry,
    CognitiveTwinSnapshot
)
from ..engine.knowledge_tracing import KnowledgeTracingEngine

router = APIRouter(prefix="/api/v1/cognitive-twin", tags=["Cognitive Twin"])

# حالياً البيانات بتتحفظ في الرامات (In-memory). ده معناه لو السيرفر عمل Restart، بيانات الطلاب هتروح. لما نيجي نوصل لمرحلة الإنتاج الفعلي، كل اللي هنعمله إننا هنبدل القاموس (LEARNER_DB) ده باستدعاء لقاعدة بيانات حقيقية زي PostgreSQL أو Redis، وباقي الكود هيفضل زي ما هو بالظبط.
# In-memory store (or persistent JSON/DB store)
LEARNER_DB: Dict[str, Dict[str, ConceptKnowledgeState]] = {}


@router.post("/interaction", response_model=ConceptKnowledgeState, status_code=status.HTTP_200_OK)
async def record_interaction(telemetry: InteractionTelemetry):
    """
    Ingests an interaction, runs BKT + Ebbinghaus update, and returns the new concept state.
    """
    learner_id = telemetry.learner_id
    concept_id = telemetry.concept_id

    if learner_id not in LEARNER_DB:
        LEARNER_DB[learner_id] = {}

    # Initialize concept state if first attempt
    if concept_id not in LEARNER_DB[learner_id]:
        LEARNER_DB[learner_id][concept_id] = ConceptKnowledgeState(
            concept_id=concept_id,
            concept_name=telemetry.concept_name,
            p_known=0.10  # BKT Prior
        )

    current_state = LEARNER_DB[learner_id][concept_id]
    
    # Process update
    updated_state = KnowledgeTracingEngine.process_interaction(current_state, telemetry)
    LEARNER_DB[learner_id][concept_id] = updated_state

    return updated_state


@router.get("/{learner_id}/snapshot", response_model=CognitiveTwinSnapshot)
async def get_cognitive_twin_snapshot(learner_id: str):
    """
    Returns the full Cognitive Twin knowledge map, applying real-time decay to all concepts.
    """
    if learner_id not in LEARNER_DB or not LEARNER_DB[learner_id]:
        raise HTTPException(status_code=404, detail="Learner Cognitive Twin not found.")

    concepts_map = {}
    mastery_scores = []

    for c_id, state in LEARNER_DB[learner_id].items():
        # Compute fresh retention decay on read
        retention, risk = KnowledgeTracingEngine.calculate_ebbinghaus_retention(
            state.last_practiced, state.memory_stability
        )
        updated = state.model_copy(update={
            "retention_rate": retention,
            "forgetting_risk": risk
        })
        concepts_map[c_id] = updated
        mastery_scores.append(updated.p_known * retention)

    overall_index = sum(mastery_scores) / len(mastery_scores) if mastery_scores else 0.0

    return CognitiveTwinSnapshot(
        learner_id=learner_id,
        last_updated=datetime.now(timezone.utc),
        concepts=concepts_map,
        overall_mastery_index=round(overall_index, 4)
    )
