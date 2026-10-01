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

# ── AI #1: Course Intelligence & Grounding Imports ──
import sys
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

try:
    from Course_Aware_RAG_Agent.api.upload_routes import router as ingestion_router
    from Course_Aware_RAG_Agent.api.outcomes_routes import router as outcomes_router
    from Course_Aware_RAG_Agent.api.graph_routes import router as graph_router
    from Course_Aware_RAG_Agent.api.vector_routes import router as vector_router
    from Course_Aware_RAG_Agent.api.rag_routes import router as rag_router
    from Course_Aware_RAG_Agent.rag.grounded_rag_engine import ClaudeGroundedRAGEngine
    from Course_Aware_RAG_Agent.models.rag_schemas import CourseRAGQueryRequest
    AI1_AVAILABLE = True
except Exception as _e:
    print(f"[Warning] AI #1 Course Intelligence module could not be loaded: {_e}")
    AI1_AVAILABLE = False

# ─────────────────────────────────────────────
# APP INIT
# ─────────────────────────────────────────────

app = FastAPI(
    title="SALI — Unified Learning Intelligence Platform (AI #1 + AI #2)",
    description=(
        "Closed-Loop Multi-Agent Learning Platform combining: "
        "AI #1: Course Intelligence & Grounding (Multimodal, Bloom CLOs, DAG, Vector RAG, Citations) "
        "AI #2: Learner Intelligence & Adaptation Engine (BKT, Ebbinghaus, Misconception, Next-Action)."
    ),
    version="2.0.0",
)

# AI #2 Routers
app.include_router(knowledge_tracing_router)
app.include_router(misconception_router)
app.include_router(assessment_router)
app.include_router(next_action_router)

# AI #1 Routers (Mounted when available)
if AI1_AVAILABLE:
    app.include_router(ingestion_router)
    app.include_router(outcomes_router)
    app.include_router(graph_router)
    app.include_router(vector_router)
    app.include_router(rag_router)


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
    
    # ── Intelligent Pedagogical Answer Evaluator ──
    import re
    sample_q = concept.get("sample_question", {})
    options = sample_q.get("options", [])
    accepted_variants = [v.lower().strip() for v in sample_q.get("accepted_text_answers", [])]
    presets = sample_q.get("misconception_presets", [])

    is_correct = False
    matched_misconception = None
    clean_msg = re.sub(r"[^\w\u0600-\u06FF\s<>=/]", " ", msg_lower).strip()

    # Known distinctive error triggers (never match on shared common words like 'visited')
    DISTINCT_MISCONCEPTIONS = {
        "c_past_simple": [
            ("goed", "Over-regularization: adding -ed to irregular 'go'"),
            ("didn't went", "Double past error after didn't"),
            ("didnt went", "Double past error after didn't"),
            ("buyed", "Adding -ed to irregular buy")
        ],
        "c_nouns_quantifiers": [
            ("many water", "Pluralizing uncountable liquids"),
            ("many milk", "Using many with uncountable milk"),
            ("some milk", "Using 'some' in negative clause"),
            ("waters", "Pluralizing uncountable water")
        ],
        "c_comparatives_superlatives": [
            ("more fast", "Using 'more' with short adjective 'fast'"),
            ("most fast", "Using 'most' with short adjective 'fast'"),
            ("more faster", "Double comparative stacking"),
            ("most fastest", "Double superlative stacking")
        ],
        "c_egypt_ecosystems": [
            ("only animal", "Excluding non-living elements from ecosystem"),
            ("animals only", "Excluding non-living elements from ecosystem")
        ],
        "c_decimals_place_value": [
            ("0.25 أكبر", "مغالطة مقارنة العدد الصحيح: اعتبار 0.25 أكبر من 0.8"),
            ("0.25 اكبر", "مغالطة مقارنة العدد الصحيح: اعتبار 0.25 أكبر من 0.8"),
            ("25 أكبر من 8", "تجاهل القيمة المكانية ومقارنة الأعداد كأعداد صحيحة"),
            ("25 اكبر من 8", "تجاهل القيمة المكانية ومقارنة الأعداد كأعداد صحيحة"),
            ("0.8 < 0.25", "عكس علامة المقارنة: 0.8 أصغر من 0.25")
        ],
        "c_unlike_fractions": [
            ("2/5", "مغالطة جمع المقامات: جمع 1+1 و 2+3"),
            ("2 / 5", "مغالطة جمع المقامات: جمع 1+1 و 2+3"),
            ("1+1=2", "جمع البسط والمقام مباشرة دون توحيد المقامات")
        ],
        "c_decimal_mult_div": [
            ("0.0475", "تحريك العلامة لليسار في عملية الضرب بدلاً من اليمين"),
            ("47.5", "الضرب في 10 بدلاً من 100")
        ],
        "c_gcf_lcm": [
            ("ع.م.أ = 24", "الخلط بين العامل والمضاعف"),
            ("ع م أ = 24", "الخلط بين العامل والمضاعف"),
            ("م.م.أ = 2", "الخلط بين العامل والمضاعف"),
            ("م م أ = 2", "الخلط بين العامل والمضاعف")
        ]
    }

    # 1. Option key or text selection
    opt_picked = None
    for idx, opt in enumerate(options, 1):
        opt_key = opt.get("key", "").lower()
        opt_text = opt.get("text", "").lower()
        if msg_lower in (opt_key, f"option {opt_key}", f"({opt_key})", str(idx), f"option {idx}"):
            opt_picked = opt
            break
        if opt_text in msg_lower or (len(msg_lower) > 5 and msg_lower == opt_text[:len(msg_lower)]):
            opt_picked = opt
            break

    if opt_picked:
        is_correct = opt_picked.get("is_correct", False)
        if not is_correct:
            matched_misconception = opt_picked.get("misconception")
    else:
        # Check distinctive misconceptions first
        concept_errors = DISTINCT_MISCONCEPTIONS.get(req.concept_id, [])
        for err_kw, err_desc in concept_errors:
            if err_kw in msg_lower:
                matched_misconception = err_desc
                is_correct = False
                break

        if not matched_misconception:
            # 2. Check accepted variants
            for variant in accepted_variants:
                if variant in msg_lower or variant in clean_msg:
                    is_correct = True
                    break

            # 3. Concept-specific semantic evaluation
            if not is_correct:
                if req.concept_id == "c_past_simple":
                    if any(v in msg_lower for v in ["visited", "went", "traveled", "travelled", "travled"]):
                        is_correct = True
                elif req.concept_id == "c_nouns_quantifiers":
                    if ("any" in msg_lower or "some" in msg_lower):
                        is_correct = True
                elif req.concept_id == "c_comparatives_superlatives":
                    if ("fastest" in msg_lower or "faster" in msg_lower):
                        is_correct = True
                elif req.concept_id == "c_egypt_ecosystems":
                    if any(w in msg_lower for w in ["erosion", "shelter", "protect", "coast", "mangrove", "تآكل", "حماية"]):
                        is_correct = True
                elif req.concept_id == "c_decimals_place_value":
                    if (">" in msg_lower or "أكبر" in msg_lower or "0.80" in msg_lower or "0.8" in msg_lower):
                        is_correct = True
                elif req.concept_id == "c_unlike_fractions":
                    if ("5/6" in msg_lower or "5 / 6" in msg_lower or "خمسة" in msg_lower):
                        is_correct = True
                elif req.concept_id == "c_decimal_mult_div":
                    if "475" in msg_lower:
                        is_correct = True
                elif req.concept_id == "c_gcf_lcm":
                    if ("2" in msg_lower and "24" in msg_lower):
                        is_correct = True

    # Determine personalized pedagogical feedback
    if is_correct:
        custom_feedback = sample_q.get("pedagogical_success_reply")
    else:
        custom_feedback = sample_q.get("pedagogical_remediation_reply")

    
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

    # ── AI #1: Dynamic Grounded RAG Query ──
    grounding_data = {
        "confidence": 0.95,
        "model_used": "Pre-grounded Course Evidence",
        "citations": [
            {
                "citation_id": "[1]",
                "source_file": "course_syllabus.pdf",
                "page_or_slide_number": 1,
                "chunk_id": f"CHK-{req.course_id}-001",
                "quoted_snippet": course_evidence[:150] + "...",
                "relevance_note": "Primary curriculum reference"
            }
        ],
        "addressed_concepts": [req.concept_id],
        "next_steps": ["Advanced Fractions", "Decimals Operations"]
    }

    if AI1_AVAILABLE:
        try:
            rag_engine = ClaudeGroundedRAGEngine()
            rag_res = rag_engine.answer_query(
                CourseRAGQueryRequest(
                    course_id=req.course_id,
                    query=f"{concept_name}: {req.student_message}",
                    top_k_chunks=3
                )
            )
            grounding_data = {
                "confidence": rag_res.grounding_confidence,
                "model_used": rag_res.model_used,
                "citations": [c.model_dump() for c in rag_res.citations],
                "addressed_concepts": rag_res.addressed_concept_ids or [req.concept_id],
                "next_steps": rag_res.pedagogical_next_steps,
                "rag_markdown_summary": rag_res.answer_markdown
            }
            if rag_res.citations:
                course_evidence = f"{rag_res.citations[0].quoted_snippet} [Doc: {rag_res.citations[0].source_file}]"
        except Exception as _rag_err:
            print(f"[RAG Grounding Error] {_rag_err}")

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
        misconception=misc_signal,
        custom_pedagogical_feedback=custom_feedback
    )


    return {
        "tutor_reply": action_plan.response_content,
        "action_type": action_plan.action_type.value,
        "reasoning": action_plan.reasoning,
        "is_correct": is_correct,
        "grounding": grounding_data,
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
