"""
Course-Aware RAG Agent (AI #1) — Main FastAPI Application
Consolidates all 5 phases of Course Intelligence & Grounding for SALI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Course_Aware_RAG_Agent.api.upload_routes import router as ingestion_router
from Course_Aware_RAG_Agent.api.outcomes_routes import router as outcomes_router
from Course_Aware_RAG_Agent.api.graph_routes import router as graph_router
from Course_Aware_RAG_Agent.api.vector_routes import router as vector_router
from Course_Aware_RAG_Agent.api.rag_routes import router as rag_router

app = FastAPI(
    title="SALI — Course Intelligence & Grounding Agent (AI #1)",
    description=(
        "Pedagogical AI Engine responsible for Multimodal Ingestion, Bloom's Taxonomy Outcomes, "
        "Concept Graph & Prerequisites DAG, Dense Vector Embeddings, and Grounded RAG with Verifiable Citations."
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all 5 phase routers
app.include_router(ingestion_router)
app.include_router(outcomes_router)
app.include_router(graph_router)
app.include_router(vector_router)
app.include_router(rag_router)


@app.get("/")
def root():
    return {
        "system": "SALI — Course Intelligence & Grounding Agent (AI #1)",
        "status": "online",
        "phases_active": [
            "1. Multimodal Content Ingestion (PDF/PPTX/Gemini Flash)",
            "2. Learning Outcomes Parsing (Bloom's Taxonomy / Claude 3.5 Sonnet)",
            "3. Concept Graph & Prerequisites (NetworkX DAG / Claude 3.5 Sonnet)",
            "4. Chunking & Vector Embeddings (OpenAI text-embedding-3-small)",
            "5. Course-Aware Grounded RAG (Claude 3.5 Sonnet Citations)"
        ],
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Course_Aware_RAG_Agent.main:app", host="127.0.0.1", port=8001, reload=True)
