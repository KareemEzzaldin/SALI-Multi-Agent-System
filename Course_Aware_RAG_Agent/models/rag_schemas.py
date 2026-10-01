"""
Course-Aware RAG Agent (AI #1) — Grounded RAG & Citations Schemas (Phase 5)
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class AcademicCitation(BaseModel):
    """Verifiable source citation grounding a specific claim in the course materials."""
    citation_id: str = Field(..., description="Citation marker, e.g. '[1]', '[2]'")
    source_file: str = Field(..., description="Filename, e.g. 'lecture_03.pdf'")
    page_or_slide_number: Optional[int] = Field(None, description="Page or slide index")
    chunk_id: str = Field(..., description="Unique chunk ID in vector database")
    quoted_snippet: str = Field(..., description="Exact textual excerpt backing the claim")
    relevance_note: Optional[str] = Field(None, description="Why this citation is authoritative")


class GroundedAnswer(BaseModel):
    """Complete grounded pedagogical answer with verifiable citations and DAG navigation."""
    course_id: str
    query: str
    answer_markdown: str = Field(..., description="Comprehensive pedagogical answer containing inline citations [1], [2]")
    citations: List[AcademicCitation] = Field(default_factory=list, description="List of cited source excerpts")
    grounding_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score reflecting strict course alignment")
    addressed_concept_ids: List[str] = Field(default_factory=list, description="Concepts covered from Phase 3 DAG")
    addressed_outcome_ids: List[str] = Field(default_factory=list, description="CLOs addressed from Phase 2")
    pedagogical_next_steps: List[str] = Field(default_factory=list, description="Recommended downstream concepts based on DAG prerequisites")
    model_used: str = Field(default="Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CourseRAGQueryRequest(BaseModel):
    """Request payload to ask a grounded course question."""
    course_id: str
    query: str = Field(..., description="Student or AI agent query")
    top_k_chunks: int = Field(default=4, ge=1, le=10)
    student_id: Optional[str] = Field(None, description="Optional student ID for personalization")
    include_concept_prerequisites: bool = Field(default=True, description="Enrich prompt with DAG prerequisites")
    academic_level: Optional[str] = "Undergraduate"
