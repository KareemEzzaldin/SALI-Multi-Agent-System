"""
Course-Aware RAG Agent (AI #1) — Learning Outcomes Schemas (Phase 2)
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class BloomTaxonomyLevel(str, Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class LearningOutcomeItem(BaseModel):
    """A granular course learning outcome (CLO / ILO)."""
    outcome_id: str = Field(..., description="Unique identifier, e.g., 'CLO-1', 'CLO-2'")
    title: str = Field(..., description="Brief outcome heading, e.g., 'Memory Reference Manipulation'")
    description: str = Field(..., description="Measurable statement of what student will be able to do")
    bloom_level: BloomTaxonomyLevel = Field(..., description="Calibrated Bloom's taxonomy tier")
    action_verbs: List[str] = Field(default_factory=list, description="Measurable action verbs, e.g. ['trace', 'differentiate']")
    target_skills: List[str] = Field(default_factory=list, description="Associated technical competencies")
    assessment_rubric_hint: str = Field(..., description="Guidance on how to evaluate this specific outcome")


class CourseOutcomesManifest(BaseModel):
    """Complete structured manifest of all parsed learning outcomes for a course."""
    course_id: str
    course_title: str
    academic_level: Optional[str] = Field(None, description="e.g. 'Undergraduate Year 2'")
    total_outcomes: int
    outcomes: List[LearningOutcomeItem]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ParseOutcomesRequest(BaseModel):
    """Payload to trigger learning outcomes parsing from syllabus text."""
    course_id: str
    course_title: str
    syllabus_text: str = Field(..., description="Raw or extracted text from syllabus/curriculum specification")
    academic_level: Optional[str] = "Undergraduate Computer Science"
