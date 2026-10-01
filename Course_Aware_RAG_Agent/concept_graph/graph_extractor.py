"""
Course-Aware RAG Agent (AI #1) — Concept Graph Extractor (Phase 3)
Optimized for Claude 3.5 Sonnet to extract Knowledge Entities, Prerequisite Edges, and DAG structures.
"""
from __future__ import annotations
import json
import os
import re
from typing import Optional, Dict, Any, List

from Course_Aware_RAG_Agent.models.concept_graph_schemas import (
    ConceptNode,
    ConceptEdge,
    ConceptRelationType,
    ConceptDifficulty,
    CourseConceptGraph,
    BuildConceptGraphRequest,
)
from Course_Aware_RAG_Agent.models.outcomes_schemas import CourseOutcomesManifest
from Course_Aware_RAG_Agent.concept_graph.dag_engine import DAGEngine

# ---------------------------------------------------------------------------
# Claude 3.5 Sonnet Prompt Architecture for Knowledge Graph & DAG
# ---------------------------------------------------------------------------

def build_claude_concept_graph_prompt(
    course_id: str,
    course_title: str,
    content: str,
    academic_level: Optional[str] = "Undergraduate",
    outcomes_manifest: Optional[CourseOutcomesManifest] = None
) -> str:
    """
    Constructs an XML-structured prompt for Claude 3.5 Sonnet to deconstruct curriculum text
    into a formal Directed Acyclic Graph (DAG) of concepts and prerequisite relationships.
    """
    outcomes_xml = ""
    if outcomes_manifest and outcomes_manifest.outcomes:
        items_str = "\n".join(
            f"    <outcome id=\"{clo.outcome_id}\" bloom=\"{clo.bloom_level.value}\">{clo.title}: {clo.description}</outcome>"
            for clo in outcomes_manifest.outcomes
        )
        outcomes_xml = f"""
<existing_learning_outcomes>
{items_str}
</existing_learning_outcomes>
"""

    prompt = f"""You are the Lead Knowledge Graph & Curriculum Architect in the SALI Multi-Agent AI System.
Your task is to analyze the course content and extract an academic Concept Graph represented as a Directed Acyclic Graph (DAG) with explicit prerequisite dependencies.

<context>
  <course_id>{course_id}</course_id>
  <course_title>{course_title}</course_title>
  <academic_level>{academic_level or 'Undergraduate'}</academic_level>
</context>
{outcomes_xml}
<pedagogical_dag_rules>
1. Node Granularity: Extract discrete, well-defined academic concepts (Concepts / Knowledge Entities). Avoid overly generic titles (e.g. use "Binary Search Tree Balancing" rather than just "Trees").
2. Explicit Prerequisites: For each edge with relation "prerequisite_of", source_id MUST be the concept that the learner needs to master FIRST, and target_id is the dependent concept that builds upon it.
3. Strict Acyclic Property (DAG): The prerequisite graph MUST NOT contain cycles! A concept cannot directly or indirectly be a prerequisite of itself. (e.g., A -> B -> C -> A is strictly forbidden).
4. Outcome Linkage: Link each concept to 1 or 2 relevant CLO outcome IDs (e.g. ["CLO-1"]) from the provided learning outcomes if available.
5. Difficulty Calibration: Assign difficulty ("beginner", "intermediate", "advanced") and realistic estimated study hours (1.0 to 10.0 hours).
6. Strict JSON Output: Output ONLY valid JSON complying with the target schema. Do not wrap in markdown or add conversational filler.
</pedagogical_dag_rules>

<target_json_schema>
{{
  "course_id": "{course_id}",
  "course_title": "{course_title}",
  "nodes": [
    {{
      "concept_id": "CON-1",
      "name": "<Concept Name>",
      "description": "<Pedagogical summary of this concept>",
      "difficulty": "beginner" | "intermediate" | "advanced",
      "estimated_learning_hours": 2.5,
      "linked_outcome_ids": ["CLO-1"],
      "key_terms": ["term1", "term2"]
    }}
  ],
  "edges": [
    {{
      "source_id": "CON-1",
      "target_id": "CON-2",
      "relation_type": "prerequisite_of" | "part_of" | "relates_to" | "extends",
      "weight": 1.0,
      "explanation": "<Why CON-1 must be understood prior to CON-2>"
    }}
  ]
}}
</target_json_schema>

<raw_course_content>
{content}
</raw_course_content>

Analyze the prerequisite dependencies thoroughly, ensure acyclic integrity, and output the JSON concept graph:"""
    return prompt


# ---------------------------------------------------------------------------
# Claude 3.5 Sonnet Graph Extractor Engine
# ---------------------------------------------------------------------------

class ClaudeConceptGraphExtractor:
    """
    Extracts structured academic concept nodes and prerequisite edges using Claude 3.5 Sonnet.
    Guarantees mathematical DAG validity and topological sort via DAGEngine.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"[ClaudeConceptGraphExtractor] Warning: Anthropic client failed: {e}")

    def build_graph(self, request: BuildConceptGraphRequest) -> CourseConceptGraph:
        """
        Builds the CourseConceptGraph from syllabus/curriculum content.
        Uses Claude 3.5 Sonnet if available, or deterministic pedagogical heuristic fallback.
        In all cases, runs NetworkX DAG sequencing to verify and order the nodes.
        """
        prompt = build_claude_concept_graph_prompt(
            course_id=request.course_id,
            course_title=request.course_title,
            content=request.course_content_or_syllabus,
            academic_level=request.academic_level,
            outcomes_manifest=request.existing_outcomes_manifest
        )

        nodes: List[ConceptNode] = []
        edges: List[ConceptEdge] = []
        meta: Dict[str, Any] = {"model_engine": "heuristic_fallback"}

        if self.client:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    temperature=0.1,
                    system="You are an expert curriculum architect. Construct clean, acyclic knowledge graphs (DAGs) of academic concepts. Output strictly valid JSON.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                raw_text = response.content[0].text
                parsed_json = self._parse_json_response(raw_text)
                
                nodes = [ConceptNode.model_validate(n) for n in parsed_json.get("nodes", [])]
                edges = [ConceptEdge.model_validate(e) for e in parsed_json.get("edges", [])]
                meta = {"model_engine": f"claude-3.5-sonnet ({self.model})"}
            except Exception as e:
                print(f"[ClaudeConceptGraphExtractor] Claude API failed: {e}. Switching to deterministic DAG fallback.")
                nodes, edges = self._fallback_extract(request)
        else:
            nodes, edges = self._fallback_extract(request)

        # Run DAG analysis & topological sequencing via DAGEngine
        return DAGEngine.analyze_and_sequence(
            course_id=request.course_id,
            course_title=request.course_title,
            nodes=nodes,
            edges=edges,
            metadata=meta
        )

    def _clean_json_str(self, text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def _parse_json_response(self, raw_text: str) -> Dict[str, Any]:
        cleaned = self._clean_json_str(raw_text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            raise ValueError("Could not parse valid JSON from LLM graph response.")

    def _fallback_extract(self, request: BuildConceptGraphRequest) -> tuple[List[ConceptNode], List[ConceptEdge]]:
        """
        Deterministic, pedagogically sound fallback graph builder when offline.
        Parses topics into a clean linear/branched dependency DAG.
        """
        lines = [line.strip() for line in request.course_content_or_syllabus.splitlines() if line.strip()]
        topic_lines = []
        for line in lines:
            cleaned = re.sub(r"^[-*•\d\.\)\s]+", "", line).strip()
            if len(cleaned) > 10 and not cleaned.lower().startswith("syllabus"):
                topic_lines.append(cleaned)

        if len(topic_lines) < 3:
            topic_lines = [
                f"Foundational Architecture of {request.course_title}",
                f"Core Data Representation & Primitive Operations in {request.course_title}",
                f"Algorithmic Control Flow & State Manipulation in {request.course_title}",
                f"Advanced Memory Structures & Concurrency in {request.course_title}",
                f"System Optimization & Scalability in {request.course_title}"
            ]

        nodes: List[ConceptNode] = []
        edges: List[ConceptEdge] = []
        difficulties = [ConceptDifficulty.BEGINNER, ConceptDifficulty.BEGINNER, ConceptDifficulty.INTERMEDIATE, ConceptDifficulty.INTERMEDIATE, ConceptDifficulty.ADVANCED]

        for i, topic in enumerate(topic_lines[:8]):
            cid = f"CON-{i+1}"
            diff = difficulties[min(i, len(difficulties) - 1)]
            hours = 1.5 + (i * 0.75)
            
            # Map to CLO if available
            clo_id = f"CLO-{i+1}" if request.existing_outcomes_manifest and i < len(request.existing_outcomes_manifest.outcomes) else "CLO-1"

            nodes.append(
                ConceptNode(
                    concept_id=cid,
                    name=topic[:40] if len(topic) > 40 else topic,
                    description=f"Core conceptual study of {topic}",
                    difficulty=diff,
                    estimated_learning_hours=hours,
                    linked_outcome_ids=[clo_id],
                    key_terms=[w for w in re.findall(r"\b[A-Za-z]{4,}\b", topic)[:4]]
                )
            )

        # Build progressive prerequisite DAG chain (e.g., CON-1 -> CON-2 -> CON-3 ...)
        for i in range(len(nodes) - 1):
            edges.append(
                ConceptEdge(
                    source_id=nodes[i].concept_id,
                    target_id=nodes[i+1].concept_id,
                    relation_type=ConceptRelationType.PREREQUISITE_OF,
                    weight=1.0,
                    explanation=f"Mastery of {nodes[i].name} is an essential foundational prerequisite before learning {nodes[i+1].name}."
                )
            )

        # Add a lateral "extends" or "relates_to" edge if more than 3 concepts
        if len(nodes) >= 4:
            edges.append(
                ConceptEdge(
                    source_id=nodes[1].concept_id,
                    target_id=nodes[3].concept_id,
                    relation_type=ConceptRelationType.EXTENDS,
                    weight=0.7,
                    explanation="Builds upon foundational state representation."
                )
            )

        return nodes, edges
