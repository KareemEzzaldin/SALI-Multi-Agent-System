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
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

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
from backend.data.courses_data import COURSES_DATA, STUDENT_PROFILE
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

# ─────────────────────────────────────────────
# PROTOTYPE STATIC SERVING
# ─────────────────────────────────────────────

PROTOTYPE_DIR = Path(__file__).parent.parent / "prototype"

if PROTOTYPE_DIR.exists():
    app.mount("/css", StaticFiles(directory=str(PROTOTYPE_DIR / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(PROTOTYPE_DIR / "js")), name="js")

@app.get("/", include_in_schema=False)
def serve_prototype():
    index_file = PROTOTYPE_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "SALI Prototype interface not found"}

@app.get("/api/courses")
def get_courses():
    return COURSES_DATA

@app.get("/api/student-profile")
def get_student_profile():
    return STUDENT_PROFILE


class ChatMessageRequest(BaseModel):
    learner_id: str = "STD-2026-904"
    course_id: str
    concept_id: str
    student_message: str
    consecutive_failures: int = 0
    attempt_number: int = 1


@app.post("/api/chat")
async def chat_with_tutor(req: ChatMessageRequest):
    """
    Natural Chat Endpoint powering the student's conversation with the 5 AI Agents:
    1. Diagnoses misconceptions in the student's message (Agent 2).
    2. Updates Bayesian Knowledge Tracing & Ebbinghaus decay (Agent 1).
    3. Selects the appropriate pedagogical response mode (Agent 4: Socratic / Remediation / Escalation / Practice).
    4. Triggers closed-loop background updates (Agent 5).
    """
    from backend.data.courses_data import COURSES_DATA
    from ai_agents import (
        CognitiveTwinAgent, ConceptState, InteractionTelemetry,
        MisconceptionDetectionAgent, AttemptRecord,
        NextBestActionAgent, ActionType
    )

    # Locate concept and course
    course = next((c for c in COURSES_DATA if c["course_id"] == req.course_id), COURSES_DATA[0])
    concept = next((c for c in course["concepts"] if c["concept_id"] == req.concept_id), course["concepts"][0])
    
    concept_name = concept["concept_name"]
    course_evidence = concept["course_evidence"]
    current_mastery = concept["mastery"]
    stability = concept["stability"]

    msg_lower = req.student_message.lower().strip()
    
    # Check if student answer is correct or reveals a misconception
    sample_q = concept.get("sample_question", {})
    correct_keywords = ["same", "reference", "address", "persist", "definition", "nonlocal", "amortized", "chaining", "log"]
    is_correct = any(kw in msg_lower for kw in correct_keywords) and not any(kw in msg_lower for kw in ["copy", "clone", "error", "overwrite", "each call", "re-initialized"])
    
    # Agent 2: Misconception Detection
    misc_signal = MisconceptionDetectionAgent.diagnose(
        concept_name=concept_name,
        attempts=[
            AttemptRecord(
                attempt_number=req.attempt_number,
                question_id=sample_q.get("question_id", "q_chat"),
                question_text=sample_q.get("question_text", f"Explain {concept_name}"),
                correct_answer=sample_q.get("correct_answer", "Correct mechanical behavior"),
                learner_answer=req.student_message,
                is_correct=is_correct
            )
        ],
        current_question=sample_q.get("question_text", f"Explain {concept_name}"),
        correct_answer=sample_q.get("correct_answer", "Correct mechanical behavior"),
        learner_answer=req.student_message,
        is_correct=is_correct,
        course_evidence=course_evidence
    )

    # Agent 1: Cognitive Twin Step (BKT + Ebbinghaus)
    state = ConceptState(
        concept_id=req.concept_id,
        concept_name=concept_name,
        p_known=current_mastery,
        memory_stability=stability
    )
    telemetry = InteractionTelemetry(
        learner_id=req.learner_id,
        concept_id=req.concept_id,
        concept_name=concept_name,
        is_correct=is_correct,
        attempt_number=req.attempt_number
    )
    updated_state = CognitiveTwinAgent.step(state, telemetry)
    if misc_signal.detected:
        updated_state = MisconceptionDetectionAgent.link_state(updated_state, misc_signal)

    # Update in-memory course concept mastery for live reflect
    delta = round(updated_state.p_known - current_mastery, 4)
    concept["mastery"] = updated_state.p_known
    concept["stability"] = updated_state.memory_stability

    # Agent 4: Next-Best Action Pedagogical Decision
    action_plan = NextBestActionAgent.prescribe(
        learner_id=req.learner_id,
        concept_name=concept_name,
        consecutive_failures=req.consecutive_failures + (0 if is_correct else 1),
        attempt_number=req.attempt_number,
        frustration_flag=req.consecutive_failures >= 2,
        is_correct=is_correct,
        p_known=updated_state.p_known,
        course_evidence=course_evidence,
        misconception=misc_signal
    )

    return {
        "tutor_reply": action_plan.response_content,
        "action_type": action_plan.action_type.value,
        "reasoning": action_plan.reasoning,
        "is_correct": is_correct,
        "misconception": {
            "detected": misc_signal.detected,
            "description": misc_signal.misunderstanding_description,
            "confidence_score": misc_signal.confidence_score,
            "category": misc_signal.category
        },
        "state_update": {
            "concept_name": concept_name,
            "new_mastery": updated_state.p_known,
            "mastery_delta": delta,
            "memory_stability_days": updated_state.memory_stability,
            "forgetting_risk": updated_state.forgetting_risk
        },
        "human_dossier": action_plan.human_dossier.model_dump() if action_plan.human_dossier else None
    }


@app.post("/api/chat/generate-question")
async def generate_chat_question(req: ChatMessageRequest):
    """
    Uses Agent 3 (Adaptive Assessment) to generate a question in the student's ZPD
    and delivers it directly into the chat session.
    """
    from backend.data.courses_data import COURSES_DATA
    from ai_agents import AdaptiveAssessmentAgent

    course = next((c for c in COURSES_DATA if c["course_id"] == req.course_id), COURSES_DATA[0])
    concept = next((c for c in course["concepts"] if c["concept_id"] == req.concept_id), course["concepts"][0])

    item = AdaptiveAssessmentAgent.generate_question(
        concept_name=concept["concept_name"],
        p_known=concept["mastery"],
        rag_evidence=concept["course_evidence"],
        known_misconception="Treating references as deep copies"
    )

    return {
        "question_id": item.question_id,
        "concept_name": concept["concept_name"],
        "difficulty": item.difficulty.value,
        "bloom_level": item.bloom_level.value,
        "question_text": item.question_text,
        "code_snippet": item.code_snippet,
        "options": [o.model_dump() for o in item.options],
        "explanation": item.pedagogical_explanation
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
