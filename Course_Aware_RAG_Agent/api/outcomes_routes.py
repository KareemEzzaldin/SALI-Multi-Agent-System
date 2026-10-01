"""
Course-Aware RAG Agent (AI #1) — Outcomes & Curriculum API Endpoints (Phase 2)
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any

from Course_Aware_RAG_Agent.models.outcomes_schemas import (
    CourseOutcomesManifest,
    ParseOutcomesRequest,
    BloomTaxonomyLevel,
)
from Course_Aware_RAG_Agent.outcomes.outcomes_parser import (
    ClaudeOutcomesParser,
    build_claude_outcomes_prompt,
)
from Course_Aware_RAG_Agent.outcomes.storage import OutcomesStorage

router = APIRouter(prefix="/api/v1/course-outcomes", tags=["Course Learning Outcomes (Phase 2)"])

storage = OutcomesStorage()
parser = ClaudeOutcomesParser()


@router.post("/parse", response_model=CourseOutcomesManifest)
def parse_syllabus_outcomes(request: ParseOutcomesRequest) -> CourseOutcomesManifest:
    """
    Parses a syllabus text into structured Course Learning Outcomes (CLOs)
    calibrated to Bloom's Revised Taxonomy using Claude 3.5 Sonnet.
    Saves the generated manifest automatically.
    """
    try:
        manifest = parser.parse(request)
        storage.save_manifest(manifest)
        return manifest
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse learning outcomes: {str(e)}")


@router.get("/prompt", response_model=Dict[str, Any])
def inspect_claude_prompt(
    course_id: str = Query("CS-201", description="Course Code"),
    course_title: str = Query("Data Structures and Algorithms", description="Course Title"),
    academic_level: str = Query("Undergraduate Year 2", description="Academic level"),
    syllabus_sample: Optional[str] = Query(None, description="Optional custom syllabus snippet")
) -> Dict[str, Any]:
    """
    Returns the exact XML-structured prompt configured for Claude 3.5 Sonnet.
    Useful for testing or auditing pedagogical prompt calibration.
    """
    sample_text = syllabus_sample or (
        "1. Understand memory management and pointers in C++.\n"
        "2. Implement singly, doubly, and circular linked lists with Big-O analysis.\n"
        "3. Analyze runtime complexity of recursion vs iteration using master theorem.\n"
        "4. Design and evaluate binary search trees and AVL balanced rotations."
    )
    prompt = build_claude_outcomes_prompt(
        course_id=course_id,
        course_title=course_title,
        syllabus_text=sample_text,
        academic_level=academic_level
    )
    return {
        "model": "Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)",
        "prompt_template": prompt,
        "parameters": {
            "temperature": 0.1,
            "max_tokens": 4000,
            "formatting": "Strict JSON Schema without Markdown wrap"
        }
    }


@router.get("/taxonomy/levels", response_model=Dict[str, Any])
def get_bloom_taxonomy_reference() -> Dict[str, Any]:
    """
    Returns reference metadata for Bloom's Revised Taxonomy tiers used in outcome calibration.
    """
    return {
        "levels": [
            {
                "level": BloomTaxonomyLevel.REMEMBER.value,
                "tier": 1,
                "definition": "Recall facts and basic concepts",
                "sample_verbs": ["define", "duplicate", "list", "memorize", "repeat", "state"]
            },
            {
                "level": BloomTaxonomyLevel.UNDERSTAND.value,
                "tier": 2,
                "definition": "Explain ideas or concepts",
                "sample_verbs": ["classify", "describe", "discuss", "explain", "identify", "locate", "recognize"]
            },
            {
                "level": BloomTaxonomyLevel.APPLY.value,
                "tier": 3,
                "definition": "Use information in new situations",
                "sample_verbs": ["execute", "implement", "solve", "use", "demonstrate", "interpret", "operate"]
            },
            {
                "level": BloomTaxonomyLevel.ANALYZE.value,
                "tier": 4,
                "definition": "Draw connections among ideas",
                "sample_verbs": ["differentiate", "organize", "relate", "compare", "contrast", "distinguish", "examine"]
            },
            {
                "level": BloomTaxonomyLevel.EVALUATE.value,
                "tier": 5,
                "definition": "Justify a stand or decision",
                "sample_verbs": ["appraise", "argue", "defend", "judge", "select", "support", "value", "critique"]
            },
            {
                "level": BloomTaxonomyLevel.CREATE.value,
                "tier": 6,
                "definition": "Produce new or original work",
                "sample_verbs": ["design", "assemble", "construct", "formulate", "author", "investigate", "develop"]
            }
        ]
    }


@router.get("/manifests", response_model=List[Dict[str, Any]])
def list_saved_manifests() -> List[Dict[str, Any]]:
    """List all persisted course learning outcome manifests."""
    return storage.list_manifests()


@router.get("/{course_id}", response_model=CourseOutcomesManifest)
def get_course_manifest(course_id: str) -> CourseOutcomesManifest:
    """Retrieve the parsed learning outcomes manifest for a specific course."""
    manifest = storage.get_manifest(course_id)
    if not manifest:
        raise HTTPException(status_code=404, detail=f"No outcomes manifest found for course '{course_id}'.")
    return manifest
