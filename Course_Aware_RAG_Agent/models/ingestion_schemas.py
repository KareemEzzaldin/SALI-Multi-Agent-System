"""
Course-Aware RAG Agent (AI #1) — Ingestion Schemas
Strictly typed Pydantic v2 schemas for multimodal course ingestion.
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ModalityType(str, Enum):
    TEXT = "text"
    SLIDE = "slide"
    TABLE = "table"
    OCR_IMAGE = "ocr_image"
    AUDIO_TRANSCRIPT = "audio_transcript"


class ExtractedSegment(BaseModel):
    """A structured content segment extracted from course materials."""
    segment_id: str
    modality: ModalityType
    content: str = Field(..., description="Clean extracted text, markdown table, or transcript")
    source_file: str
    page_or_slide_num: Optional[int] = Field(None, description="Page number for PDF or slide index for PPTX")
    timestamp_range: Optional[str] = Field(None, description="E.g. '01:30 - 03:45' for audio/video")
    diagram_description: Optional[str] = Field(None, description="Visual description if segment is a chart/diagram")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestionResponse(BaseModel):
    """Unified API response after ingesting a course material."""
    document_id: str
    file_name: str
    file_type: str
    total_pages_or_slides: int
    total_segments: int
    total_characters: int
    segments: List[ExtractedSegment]
    ingestion_summary: str
