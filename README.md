# 🎓 SALI / SLA Multi-Agent Learning Intelligence Platform

A state-of-the-art Cognitive Twin & Adaptive Learning System built with clean separation of concerns between **Pure AI Modeling** and **Pure Software Engineering**.

---

## 🏛️ System Architecture

```
├── SLA system/                    # 💻 Pure Software Engineering Layer
│   ├── backend/                   # FastAPI REST microservices & controllers
│   ├── prototype/                 # Interactive Student Portal (HTML/CSS/JS)
│   ├── run_server.py              # 1-Click Server & Web Launcher
│   └── requirements.txt           # Web & software dependencies
│
├── Cognitive_Twin_AI_Agent/       # 🧠 Pure AI: Cognitive Twin & Adaptation Layer
│   ├── ai_agents/                 # The 5 Pedagogical Multi-Agent System:
│   │   ├── cognitive_twin_agent.py      # Bayesian Knowledge Tracing (BKT) & Ebbinghaus
│   │   ├── misconception_agent.py       # Error Diagnosis & Misconception State Linking
│   │   ├── adaptive_assessment_agent.py # ZPD & Bloom's Taxonomy Dynamic Calibrator
│   │   ├── next_action_agent.py         # Pedagogical Decision Trees & Socratic Tutor
│   │   └── closed_loop_agent.py         # End-to-End Learning Cycle Pipeline
│   └── requirements.txt           # AI dependencies (OpenAI, Anthropic, NumPy, Pydantic)
│
└── Course_Aware_RAG_Agent/        # 📚 Pure AI: Course Intelligence & RAG
    ├── concept_graph/             # Curriculum concept knowledge graph
    ├── vector_store/              # Vector database & semantic embeddings
    ├── rag/                       # Grounded RAG engines
    ├── multimodal/                # Multimodal slides & PDF ingesters
    └── requirements.txt           # Multimodal RAG dependencies
```

---

## ⚡ Quick Start

### Start the SLA Web Platform
```bash
cd "SLA system"
python run_server.py
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.
