# 💻 SLA System (Software Layer & Student Learning Assistant Portal)

This directory contains the entire **Pure Software Architecture** for the SALI / SLA Learning Intelligence Platform.

It isolates all web engineering, REST API services, state management, and front-end user experience from the pure AI engine.

---

## 📁 System Architecture

```
SLA system/
├── backend/                    # FastAPI Microservices & Application Layer
│   ├── main.py                 # FastAPI Application Root & Route Mounting
│   ├── api/                    # REST API Controllers (Assessment, Knowledge Tracing, Misconceptions, Next-Action)
│   ├── data/                   # Data Stores, Curriculum Repositories (Connect 5 & Primary 5 Math), and Student Profiles
│   │   ├── courses_data.py     # Curriculum data, question banks, and student cognitive dossier
│   │   └── state/              # Persistent student state JSON files
│   ├── engine/                 # Software pipeline and execution glue
│   └── models/                 # Pydantic v2 schemas for API requests & responses
├── prototype/                  # Clean, Responsive Web Portal (Frontend)
│   ├── index.html              # Single Page Application (SPA) student chat & dossier interface
│   ├── css/
│   │   └── portal.css          # Modern dark-mode UI styles & responsive layout
│   └── js/
│       └── portal.js           # Interactive client-side controller (Chat, BKT radar, modal)
├── run_server.py               # 1-Click Server Launcher
└── requirements.txt            # Software dependencies (FastAPI, Uvicorn, Pydantic)
```

---

## 🚀 Running the SLA System

### Option 1: Using the 1-Click Launcher
```bash
cd "SLA system"
python run_server.py
```

### Option 2: Using Uvicorn Directly
```bash
cd "SLA system"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Once started, open:
👉 **Student Portal & Chat Interface:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
👉 **Interactive API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
👉 **Student Profile Endpoint:** [http://127.0.0.1:8000/api/student-profile](http://127.0.0.1:8000/api/student-profile)
