"""
Course-Aware RAG Agent (AI #1) — Vector Chunking & Embeddings API Endpoints (Phase 4)
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

from Course_Aware_RAG_Agent.models.vector_schemas import (
    CourseChunk,
    VectorSearchResult,
    VectorQueryRequest,
    IndexCourseContentRequest,
)
from Course_Aware_RAG_Agent.models.ingestion_schemas import ModalityType
from Course_Aware_RAG_Agent.vector_store.pedagogical_chunker import PedagogicalChunker
from Course_Aware_RAG_Agent.vector_store.openai_embeddings import OpenAIEmbeddingsGenerator
from Course_Aware_RAG_Agent.vector_store.in_memory_vector_store import CourseVectorStore
from Course_Aware_RAG_Agent.concept_graph.storage import ConceptGraphStorage

router = APIRouter(prefix="/api/v1/course-vector", tags=["Vector Chunking & Embeddings (Phase 4)"])

# Shared storage and services
graph_storage = ConceptGraphStorage()
embedder = OpenAIEmbeddingsGenerator()


def _get_store(course_id: str) -> CourseVectorStore:
    store = CourseVectorStore(course_id=course_id, embeddings_generator=embedder)
    store.load_index()
    return store


@router.post("/index", response_model=Dict[str, Any])
def index_course_materials(request: IndexCourseContentRequest) -> Dict[str, Any]:
    """
    Chunks course materials into pedagogical segments, computes dense OpenAI vector embeddings (1536-dim),
    and indexes them for semantic search.
    """
    try:
        # Load concept graph if available to link concepts to chunks
        concept_graph = graph_storage.get_graph(request.course_id)
        chunker = PedagogicalChunker(config=request.chunking_config)
        store = _get_store(request.course_id)

        all_new_chunks: List[CourseChunk] = []

        for block in request.content_blocks:
            content = block.get("content", "")
            source = block.get("source")
            page_no = block.get("page_number")
            raw_mod = block.get("modality", "text")
            try:
                mod = ModalityType(raw_mod)
            except ValueError:
                mod = ModalityType.TEXT


            chunks = chunker.chunk_content(
                course_id=request.course_id,
                content=content,
                source_filename=source,
                page_or_slide_number=page_no,
                modality_source=mod,
                concept_graph=concept_graph
            )
            all_new_chunks.extend(chunks)

        indexed_count = store.add_chunks(all_new_chunks)
        stats = store.get_stats()

        return {
            "status": "success",
            "message": f"Successfully chunked and embedded {indexed_count} segments.",
            "course_id": request.course_id,
            "new_chunks_indexed": indexed_count,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index course material: {str(e)}")


@router.post("/query", response_model=List[VectorSearchResult])
def query_course_vectors(request: VectorQueryRequest) -> List[VectorSearchResult]:
    """
    Executes dense cosine vector search over indexed course chunks with optional concept filters.
    """
    store = _get_store(request.course_id)
    if not store.chunks:
        raise HTTPException(
            status_code=404,
            detail=f"No vector index found for course '{request.course_id}'. Please index content first."
        )

    results = store.search(
        query_text=request.query_text,
        top_k=request.top_k,
        min_similarity=request.min_similarity,
        filter_concept_ids=request.filter_concept_ids
    )
    return results


@router.get("/{course_id}/stats", response_model=Dict[str, Any])
def get_vector_index_stats(course_id: str) -> Dict[str, Any]:
    """Retrieves metadata and statistics for a course's vector index."""
    store = _get_store(course_id)
    if not store.chunks:
        raise HTTPException(status_code=404, detail=f"No vector index found for course '{course_id}'.")
    return store.get_stats()


@router.get("/spec", response_model=Dict[str, Any])
def get_embeddings_specification() -> Dict[str, Any]:
    """Returns technical specifications for the OpenAI embedding pipeline."""
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-small",
        "vector_dimensions": 1536,
        "similarity_metric": "Cosine Similarity (dot product on L2-normalized unit vectors)",
        "features": [
            "Matryoshka representation learning support",
            "High MTEB benchmark retrieval ranking",
            "Sub-word tokenizer and vocabulary awareness",
            "Pedagogical concept-tagging integration"
        ]
    }
