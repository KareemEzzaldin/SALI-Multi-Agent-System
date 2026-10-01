"""
Course-Aware RAG Agent (AI #1) — Concept Graph & Prerequisites Schemas (Phase 3)
Strictly typed for Pydantic v2.
"""
from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from Course_Aware_RAG_Agent.models.outcomes_schemas import CourseOutcomesManifest


class ConceptRelationType(str, Enum):
    PREREQUISITE_OF = "prerequisite_of"   # Source must be learned before Target
    PART_OF = "part_of"                   # Source is a sub-concept of Target
    RELATES_TO = "relates_to"             # Cross-cutting conceptual link
    EXTENDS = "extends"                   # Advanced specialization of Source


class ConceptDifficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ConceptNode(BaseModel):
    """An academic concept entity within a course."""
    concept_id: str = Field(..., description="Unique slug or ID, e.g., 'CON-1' or 'pointers_references'")
    name: str = Field(..., description="Display title of the concept")
    description: str = Field(..., description="Concise pedagogical summary of what this concept entails")
    difficulty: ConceptDifficulty = Field(default=ConceptDifficulty.INTERMEDIATE)
    estimated_learning_hours: float = Field(default=2.0, ge=0.5, le=40.0)
    linked_outcome_ids: List[str] = Field(default_factory=list, description="IDs of linked CLOs from Phase 2")
    key_terms: List[str] = Field(default_factory=list, description="Technical keywords and vocabulary")


class ConceptEdge(BaseModel):
    """A directed relationship between two academic concepts."""
    source_id: str = Field(..., description="Source concept ID (e.g. prerequisite)")
    target_id: str = Field(..., description="Target concept ID (e.g. dependent concept)")
    relation_type: ConceptRelationType = Field(default=ConceptRelationType.PREREQUISITE_OF)
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Dependency strength (1.0 = strict blocking prereq)")
    explanation: Optional[str] = Field(None, description="Pedagogical justification for this relation")


class CourseConceptGraph(BaseModel):
    """Complete Directed Acyclic Graph (DAG) of course concepts and prerequisites."""
    course_id: str
    course_title: str
    nodes: List[ConceptNode]
    edges: List[ConceptEdge]
    is_dag: bool = Field(..., description="True if graph is strictly acyclic")
    topological_learning_path: List[str] = Field(
        default_factory=list,
        description="Concept IDs ordered in the optimal pedagogical sequence"
    )
    detected_cycles: List[List[str]] = Field(
        default_factory=list,
        description="Any circular dependencies detected (empty if valid DAG)"
    )
    root_concepts: List[str] = Field(
        default_factory=list,
        description="Concepts with no prerequisites (entry points for learners)"
    )
    terminal_concepts: List[str] = Field(
        default_factory=list,
        description="Advanced capstone concepts at the end of the prerequisite chain"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BuildConceptGraphRequest(BaseModel):
    """Payload to extract and build a concept graph from course materials or syllabus."""
    course_id: str
    course_title: str
    course_content_or_syllabus: str = Field(..., description="Detailed syllabus, topic outline, or extracted slide text")
    academic_level: Optional[str] = "Undergraduate Computer Science"
    existing_outcomes_manifest: Optional[CourseOutcomesManifest] = None
