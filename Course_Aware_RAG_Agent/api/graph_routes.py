"""
Course-Aware RAG Agent (AI #1) — Concept Graph & DAG API Endpoints (Phase 3)
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any

from Course_Aware_RAG_Agent.models.concept_graph_schemas import (
    CourseConceptGraph,
    BuildConceptGraphRequest,
)
from Course_Aware_RAG_Agent.concept_graph.graph_extractor import (
    ClaudeConceptGraphExtractor,
    build_claude_concept_graph_prompt,
)
from Course_Aware_RAG_Agent.concept_graph.storage import ConceptGraphStorage
from Course_Aware_RAG_Agent.outcomes.storage import OutcomesStorage

router = APIRouter(prefix="/api/v1/course-graph", tags=["Concept Graph & Prerequisites (Phase 3)"])

graph_storage = ConceptGraphStorage()
outcomes_storage = OutcomesStorage()
extractor = ClaudeConceptGraphExtractor()


@router.post("/build", response_model=CourseConceptGraph)
def build_course_concept_graph(request: BuildConceptGraphRequest) -> CourseConceptGraph:
    """
    Extracts academic concepts and prerequisite relationships using Claude 3.5 Sonnet.
    Mathematically validates acyclic DAG properties and computes the optimal topological learning path.
    """
    try:
        # If existing_outcomes_manifest is not supplied in request, check if already stored on disk
        if not request.existing_outcomes_manifest:
            saved_manifest = outcomes_storage.get_manifest(request.course_id)
            if saved_manifest:
                request.existing_outcomes_manifest = saved_manifest

        graph = extractor.build_graph(request)
        graph_storage.save_graph(graph)
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to construct concept graph: {str(e)}")


@router.get("/prompt", response_model=Dict[str, Any])
def inspect_claude_graph_prompt(
    course_id: str = Query("CS-201", description="Course Code"),
    course_title: str = Query("Data Structures and Algorithms", description="Course Title"),
    academic_level: str = Query("Undergraduate Year 2", description="Academic level"),
    sample_content: Optional[str] = Query(None, description="Optional custom content sample")
) -> Dict[str, Any]:
    """
    Inspect the exact XML prompt template designed for Claude 3.5 Sonnet.
    """
    content = sample_content or (
        "Topic 1: Primitive Memory & Pointer Operations\n"
        "Topic 2: Node Chains & Linked Lists\n"
        "Topic 3: Binary Search Trees & AVL Rotations\n"
        "Topic 4: Graph Traversals (BFS, DFS) and Shortest Paths"
    )
    prompt = build_claude_concept_graph_prompt(
        course_id=course_id,
        course_title=course_title,
        content=content,
        academic_level=academic_level
    )
    return {
        "model": "Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)",
        "prompt_template": prompt,
        "parameters": {
            "temperature": 0.1,
            "max_tokens": 4000,
            "acyclic_enforcement": "Mathematical NetworkX cycle detection + topological sequencing"
        }
    }


@router.get("/{course_id}", response_model=CourseConceptGraph)
def get_concept_graph(course_id: str) -> CourseConceptGraph:
    """Retrieve the concept graph and DAG properties for a course."""
    graph = graph_storage.get_graph(course_id)
    if not graph:
        raise HTTPException(status_code=404, detail=f"No concept graph found for course '{course_id}'.")
    return graph


@router.get("/{course_id}/learning-path", response_model=Dict[str, Any])
def get_topological_learning_path(course_id: str) -> Dict[str, Any]:
    """
    Returns the step-by-step ordered pedagogical learning path based on DAG topological sort.
    """
    graph = graph_storage.get_graph(course_id)
    if not graph:
        raise HTTPException(status_code=404, detail=f"No concept graph found for course '{course_id}'.")

    node_map = {n.concept_id: n for n in graph.nodes}
    path_steps = []
    accumulated_hours = 0.0

    for step_num, cid in enumerate(graph.topological_learning_path, 1):
        node = node_map.get(cid)
        if node:
            accumulated_hours += node.estimated_learning_hours
            # Find immediate prerequisites
            prereqs = [e.source_id for e in graph.edges if e.target_id == cid and e.relation_type.value == "prerequisite_of"]
            path_steps.append({
                "step": step_num,
                "concept_id": cid,
                "name": node.name,
                "difficulty": node.difficulty.value,
                "estimated_hours": node.estimated_learning_hours,
                "accumulated_hours": accumulated_hours,
                "prerequisites": prereqs,
                "linked_clos": node.linked_outcome_ids
            })

    return {
        "course_id": course_id,
        "course_title": graph.course_title,
        "is_dag": graph.is_dag,
        "total_concepts": len(path_steps),
        "total_estimated_hours": accumulated_hours,
        "learning_path": path_steps
    }


@router.get("/list/all", response_model=List[Dict[str, Any]])
def list_saved_graphs() -> List[Dict[str, Any]]:
    """List all saved concept graphs."""
    return graph_storage.list_graphs()
