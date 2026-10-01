"""
SLA System Launcher (Backend Server & Prototype Portal)
"""
import sys
import os
from pathlib import Path
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent
COGNITIVE_TWIN_ROOT = WORKSPACE_ROOT / "Cognitive_Twin_AI_Agent"

for p in [str(BASE_DIR), str(WORKSPACE_ROOT), str(COGNITIVE_TWIN_ROOT), str(COGNITIVE_TWIN_ROOT / "ai_agents")]:
    if p not in sys.path:
        sys.path.insert(0, p)

if __name__ == "__main__":
    print("[SLA System] Starting backend server and prototype portal on http://127.0.0.1:8000 ...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
