# 🧠 Cognitive Twin AI Agent (Pure AI Cognitive Layer)

This directory is dedicated strictly to the **Pure AI Agents and Cognitive Modeling Layer** (zero web/UI bloat).

All web servers, REST API routes, and interactive frontend prototypes have been isolated into [`SLA system/`](../SLA%20system).

---

## 📁 Pure AI Architecture & Structure

```
Cognitive_Twin_AI_Agent/
├── ai_agents/                       # Standalone pure Python AI Agents (Zero web dependencies)
│   ├── __init__.py                  # Unified package exports
│   ├── cognitive_twin_agent.py      # Agent 1: BKT & Ebbinghaus forgetting curve (R = e^-t/S)
│   ├── misconception_agent.py       # Agent 2: Error pattern analysis & cognitive state linking
│   ├── adaptive_assessment_agent.py # Agent 3: ZPD & Bloom's taxonomy difficulty calibration
│   ├── next_action_agent.py         # Agent 4: Pedagogical decision rules & Socratic tutor prompts
│   ├── closed_loop_agent.py         # Agent 5: End-to-end learning cycle pipeline & webhooks
│   └── README.md                    # Quickstart and Python usage guide
└── requirements.txt                 # Pure AI dependencies (pydantic, numpy, openai, anthropic)
```

---

## 🚀 Standalone Python Usage

```python
from ai_agents import (
    CognitiveTwinAgent, ConceptState,
    ClosedLoopOrchestratorAgent
)

# 1. Initialize student concept state
state = ConceptState(concept_id="c_math_p5_01", concept_name="Place Value & Decimals")

# 2. Run an adaptive learning cycle
result = ClosedLoopOrchestratorAgent.run_cycle(
    learner_id="STD-PRI5-104",
    concept_id="c_math_p5_01",
    concept_name="Place Value & Decimals",
    current_state=state,
    attempts=[],
    current_question="In 45.678, what is the value of 7?",
    correct_answer="0.07",
    learner_answer="0.7",
    is_correct=False,
    course_evidence="The digit 7 is in the hundredths place.",
    attempt_number=1
)

print(f"Updated Mastery (BKT): {result.updated_cognitive_state.p_known:.2f}")
print(f"Prescribed Pedagogical Action: {result.prescribed_action.action_type.value}")
```

---

## 🔗 Software Layer Link

For the interactive Web UI and FastAPI backend server, see:
👉 **[`SLA system/`](../SLA%20system)**
