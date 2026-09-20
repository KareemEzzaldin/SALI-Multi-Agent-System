# 🧠 Cognitive Twin AI Agent (Learner Intelligence & Adaptation Engine)

This module represents the **Cognitive Twin & Adaptation Engine** for adaptive learning platforms.

It models the student's evolving knowledge state, detects underlying cognitive misconceptions, calibrates question difficulty in the Zone of Proximal Development (ZPD), and executes pedagogical decision trees (Escalation, Remediation, Socratic Tutoring, Practice).

---

## 📁 Architecture & Structure

```
Cognitive_Twin_AI_Agent/
├── ai_agents/                  # Standalone pure Python AI Agents (zero web dependencies)
│   ├── __init__.py             # Unified package export
│   ├── cognitive_twin_agent.py # BKT & Ebbinghaus forgetting curve (R = e^-t/S)
│   ├── misconception_agent.py  # Error pattern analysis & state linking
│   ├── adaptive_assessment_agent.py # ZPD & Bloom's taxonomy difficulty calibration
│   ├── next_action_agent.py    # Pedagogical decision rules & tutor prompts
│   ├── closed_loop_agent.py    # End-to-end learning cycle pipeline & webhooks
│   └── README.md               # Quickstart and Python usage guide
├── backend/                    # FastAPI Microservice & API Endpoints
│   ├── main.py                 # FastAPI application root
│   ├── api/                    # Modular REST endpoints
│   ├── engine/                 # Engine implementations
│   └── models/                 # Strictly typed Pydantic v2 schemas
└── requirements.txt            # Dependency specifications
```

---

## 🚀 Quick Usage (Python Standalone)

```python
from Cognitive_Twin_AI_Agent.ai_agents import (
    CognitiveTwinAgent, ConceptState,
    ClosedLoopOrchestratorAgent
)

# Initialize concept state
state = ConceptState(concept_id="c_python_ptr", concept_name="Pointers & Memory")

# Run an adaptive learning cycle
result = ClosedLoopOrchestratorAgent.run_cycle(
    learner_id="student_101",
    concept_id="c_python_ptr",
    concept_name="Pointers & Memory",
    current_state=state,
    attempts=[],
    current_question="How are pointers assigned?",
    correct_answer="By memory reference",
    learner_answer="By value copy",
    is_correct=False,
    course_evidence="Pointers pass memory addresses by reference without duplicating data.",
    attempt_number=1
)

print(f"Updated Mastery: {result.updated_cognitive_state.p_known}")
print(f"Prescribed Action: {result.prescribed_action.action_type.value}")
```

---

## ⚡ Running the FastAPI Engine

```bash
cd Cognitive_Twin_AI_Agent
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
