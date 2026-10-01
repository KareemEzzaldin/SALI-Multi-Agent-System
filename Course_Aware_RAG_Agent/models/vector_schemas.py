"""
Course-Aware RAG Agent (AI #1) — Vector Chunking & Embeddings Schemas (Phase 4)
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from Course_Aware_RAG_Agent.models.ingestion_schemas import ModalityType


class ChunkingConfig(BaseModel):
    """Configuration for pedagogical semantic text chunking."""
    chunk_size_tokens: int = Field(default=350, ge=50, le=2000, description="Target token count per chunk")
    chunk_overlap_tokens: int = Field(default=50, ge=0, le=500, description="Token overlap between consecutive chunks")
    respect_sentence_boundaries: bool = Field(default=True, description="Keep sentences intact")


class CourseChunk(BaseModel):
    """A semantic chunk of course content enriched with pedagogical metadata."""
    chunk_id: str = Field(..., description="Unique chunk identifier, e.g., 'CHK-CS201-001'")
    course_id: str
    content: str = Field(..., description="The textual chunk content")
    modality_source: ModalityType = Field(default=ModalityType.TEXT)
    source_filename: Optional[str] = None
    page_or_slide_number: Optional[int] = None
    token_count: int = Field(default=0)
    linked_concept_ids: List[str] = Field(default_factory=list, description="Associated concept IDs from Phase 3")
    linked_outcome_ids: List[str] = Field(default_factory=list, description="Associated CLO IDs from Phase 2")
    embedding: Optional[List[float]] = Field(default=None, description="OpenAI text-embedding-3-small dense vector")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VectorSearchResult(BaseModel):
    """A single semantic search match with relevance scoring."""
    chunk: CourseChunk
    similarity_score: float = Field(..., ge=-1.0, le=1.0, description="Cosine similarity score")


class VectorQueryRequest(BaseModel):
    """Search request to retrieve relevant course chunks."""
    course_id: str
    query_text: str = Field(..., description="Student or AI query, e.g. 'How do AVL tree rotations work?'")
    top_k: int = Field(default=4, ge=1, le=20)
    min_similarity: float = Field(default=0.3, ge=0.0, le=1.0)
    filter_concept_ids: Optional[List[str]] = Field(default=None, description="Optional concept filters")


class IndexCourseContentRequest(BaseModel):
    """Request to chunk, embed, and index course material."""
    course_id: str
    course_title: str
    content_blocks: List[Dict[str, Any]] = Field(
        ...,
        description="List of text items, each containing 'content', and optional 'source', 'page_number', 'modality'"
    )
    chunking_config: Optional[ChunkingConfig] = Field(default_factory=ChunkingConfig)
