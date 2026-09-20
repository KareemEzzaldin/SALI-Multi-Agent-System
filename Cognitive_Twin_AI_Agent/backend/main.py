"""
SALI — FastAPI Main Application
Learner Intelligence & Adaptation Engine (AI #2)

Endpoints:
  GET  /              → serves the frontend dashboard
  GET  /health        → service health check
  GET  /demo/{id}     → returns pre-seeded learner scenario
  POST /analyze       → core AI engine endpoint
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ConceptMastery,
    LearnerHistory,
)
from backend.engine.misconception import detect_misconception
from backend.engine.cognitive_twin import compute_cognitive_twin_update
from backend.engine.next_action import select_next_action
from backend.engine.closed_loop_pipeline import ClosedLoopPipeline
from backend.data.mock_data import LEARNER_PERSONAS
from backend.api.knowledge_tracing_routes import router as knowledge_tracing_router
from backend.api.misconception_routes import router as misconception_router
from backend.api.assessment_routes import router as assessment_router
from backend.api.next_action_routes import router as next_action_router

# ─────────────────────────────────────────────
# APP INIT
# ─────────────────────────────────────────────

app = FastAPI(
    title="SALI — Learner Intelligence & Adaptation Engine",
    description=(
        "AI #2 of the SALI Closed-Loop Learning Platform. "
        "Detects misconceptions, updates the Cognitive Twin, "
        "and determines the next-best pedagogical action."
    ),
    version="1.0.0",
)

app.include_router(knowledge_tracing_router)
app.include_router(misconception_router)
app.include_router(assessment_router)
app.include_router(next_action_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "SALI — Learner Intelligence & Adaptation Engine (AI #2)",
        "version": "1.0.0",
        "modules": [
            "ai_agents.cognitive_twin_agent",
            "ai_agents.misconception_agent",
            "ai_agents.adaptive_assessment_agent",
            "ai_agents.next_action_agent",
            "ai_agents.closed_loop_agent"
        ]
    }

# ─────────────────────────────────────────────
# PERSISTENCE — JSON FILE STORE
# ─────────────────────────────────────────────

STATE_DIR = Path(__file__).parent / "data" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)


def _state_path(learner_id: str) -> Path:
    return STATE_DIR / f"{learner_id}.json"


def load_learner_state(learner_id: str) -> Dict[str, Any] | None:
    path = _state_path(learner_id)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_learner_state(learner_id: str, mastery_vector: list) -> None:
    path = _state_path(learner_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(mastery_vector, f, indent=2)


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

def _get_mastery_score(
    mastery_vector: list[ConceptMastery], concept_name: str
) -> float:
    entry = next(
        (c for c in mastery_vector if c.concept_name.lower() == concept_name.lower()),
        None,
    )
    return entry.mastery_score if entry else 0.0


def _get_attempt_number(
    attempts: list, question_id: str, is_current_correct: bool
) -> int:
    """Count previous attempts on this question + 1 for current."""
    prev = sum(1 for a in attempts if a.question_id == question_id)
    return prev + 1


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "SALI AI Engine v1.0"}


@app.get("/demo/{learner_id}")
def get_demo(learner_id: str):
    """Return a pre-seeded demo scenario for the given learner persona."""
    if learner_id not in LEARNER_PERSONAS:
        raise HTTPException(
            status_code=404,
            detail=f"Demo persona '{learner_id}' not found. "
                   f"Available: {list(LEARNER_PERSONAS.keys())}",
        )
    return LEARNER_PERSONAS[learner_id]


@app.get("/demo-ids")
def list_demo_ids():
    """List available demo learner personas with names."""
    return [
        {
            "id": pid,
            "name": data["learner_history"]["learner_name"],
        }
        for pid, data in LEARNER_PERSONAS.items()
    ]


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """
    Core AI Engine endpoint (Step 5 Closed-Loop Feedback).
    Delegates to ClosedLoopPipeline:
    1. Knowledge Tracing & Memory Decay
    2. Misconception Pattern Analysis
    3. Next-Best Action Pedagogical Selection
    4. Asynchronous State Persistence & Webhooks via BackgroundTasks
    5. Returns strictly-typed AnalyzeResponse
    """
    return ClosedLoopPipeline.execute(
        request=request,
        persisted_state_loader=load_learner_state,
        persisted_state_saver=save_learner_state,
        background_tasks=background_tasks
    )
