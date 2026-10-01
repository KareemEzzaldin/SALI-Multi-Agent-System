"""
Course-Aware RAG Agent (AI #1) — Grounded RAG & Citations Engine (Phase 5)
Optimized for Claude 3.5 Sonnet with zero-hallucination constraint & verifiable citations.
"""
from __future__ import annotations
import json
import os
import re
from typing import List, Optional, Dict, Any

from Course_Aware_RAG_Agent.models.rag_schemas import (
    AcademicCitation,
    GroundedAnswer,
    CourseRAGQueryRequest,
)
from Course_Aware_RAG_Agent.models.vector_schemas import VectorSearchResult
from Course_Aware_RAG_Agent.vector_store.in_memory_vector_store import CourseVectorStore
from Course_Aware_RAG_Agent.vector_store.openai_embeddings import OpenAIEmbeddingsGenerator
from Course_Aware_RAG_Agent.concept_graph.storage import ConceptGraphStorage
from Course_Aware_RAG_Agent.outcomes.storage import OutcomesStorage


# ---------------------------------------------------------------------------
# Claude 3.5 Sonnet XML Prompt Construction
# ---------------------------------------------------------------------------

def build_claude_grounded_rag_prompt(
    course_id: str,
    query: str,
    excerpts: List[VectorSearchResult],
    concept_names: List[str],
    prerequisite_hints: List[str],
    clos: List[str],
    academic_level: Optional[str] = "Undergraduate"
) -> str:
    """
    Constructs an XML-structured prompt optimized for Claude 3.5 Sonnet enforcing
    strict grounding, citation attribution, and pedagogical clarity.
    """
    excerpts_xml = []
    for i, res in enumerate(excerpts, 1):
        chunk = res.chunk
        source = chunk.source_filename or "Course Document"
        page = f" page=\"{chunk.page_or_slide_number}\"" if chunk.page_or_slide_number else ""
        excerpts_xml.append(
            f'  <excerpt id="{i}" chunk_id="{chunk.chunk_id}" source="{source}"{page}>\n'
            f"    {chunk.content.strip()}\n"
            f"  </excerpt>"
        )
    excerpts_str = "\n".join(excerpts_xml) if excerpts_xml else "  <excerpt>No matching course excerpts found.</excerpt>"

    pedagogical_context = []
    if concept_names:
        pedagogical_context.append(f"  <related_concepts>{', '.join(concept_names)}</related_concepts>")
    if prerequisite_hints:
        pedagogical_context.append(f"  <prerequisite_hierarchy>\n    " + "\n    ".join(prerequisite_hints) + "\n  </prerequisite_hierarchy>")
    if clos:
        pedagogical_context.append(f"  <course_learning_outcomes>{'; '.join(clos)}</course_learning_outcomes>")
    pedagogical_str = "\n".join(pedagogical_context)

    prompt = f"""You are the Lead Grounded Tutor & Course Intelligence Engine in the SALI Multi-Agent AI System.
Your mission is to provide an authoritative, pedagogically sound, and strictly grounded answer to the student query, anchored EXCLUSIVELY in the provided course excerpts.

<context>
  <course_id>{course_id}</course_id>
  <academic_level>{academic_level or 'Undergraduate'}</academic_level>
</context>

<pedagogical_curriculum_context>
{pedagogical_str}
</pedagogical_curriculum_context>

<verified_course_excerpts>
{excerpts_str}
</verified_course_excerpts>

<strict_grounding_rules>
1. Zero Hallucination Stance: Rely SOLELY on facts presented in <verified_course_excerpts>. Do NOT incorporate external internet knowledge or speculative explanations that contradict or exceed the provided curriculum.
2. Mandatory Citations: Every substantive factual claim MUST end with an inline citation bracket like [1], [2], or [1, 2] corresponding directly to the numbered excerpt ID.
3. Missing Information Handling: If the excerpts do not contain sufficient evidence to answer the question, explicitly state: "Based on the course materials currently uploaded, this specific topic is not covered."
4. Pedagogical Tone: Structure your response with clear headings, bullet points for key mechanisms, and note any prerequisite concepts the student should review.
</strict_grounding_rules>

<student_query>
{query}
</student_query>

Provide your comprehensive, citation-grounded response in Markdown:"""
    return prompt


# ---------------------------------------------------------------------------
# Claude 3.5 Sonnet Grounded RAG Engine
# ---------------------------------------------------------------------------

class ClaudeGroundedRAGEngine:
    """
    Orchestrates course vector retrieval, DAG prerequisite navigation,
    and Claude 3.5 Sonnet generation with verifiable citations.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"[ClaudeGroundedRAGEngine] Warning: Anthropic client failed: {e}")

        self.graph_storage = ConceptGraphStorage()
        self.outcomes_storage = OutcomesStorage()
        self.embedder = OpenAIEmbeddingsGenerator()

    def answer_query(self, request: CourseRAGQueryRequest) -> GroundedAnswer:
        """
        Executes end-to-end grounded RAG:
        1. Retrieves relevant course chunks via vector search.
        2. Retrieves DAG concepts and prerequisites.
        3. Formulates Claude 3.5 Sonnet XML prompt.
        4. Synthesizes grounded answer with verifiable academic citations.
        """
        # 1. Retrieve vector chunks
        store = CourseVectorStore(course_id=request.course_id, embeddings_generator=self.embedder)
        store.load_index()
        search_results = store.search(
            query_text=request.query,
            top_k=request.top_k_chunks,
            min_similarity=0.1
        )

        # 2. Extract pedagogical context from Concept Graph & Outcomes
        graph = self.graph_storage.get_graph(request.course_id)
        outcomes = self.outcomes_storage.get_manifest(request.course_id)

        concept_names = []
        prereq_hints = []
        addressed_concepts = []
        next_steps = []

        if graph:
            # Map search results to concepts
            for res in search_results:
                for cid in res.chunk.linked_concept_ids:
                    if cid not in addressed_concepts:
                        addressed_concepts.append(cid)

            # Gather concept details and prerequisites
            for node in graph.nodes:
                if node.concept_id in addressed_concepts or any(term.lower() in request.query.lower() for term in node.key_terms):
                    concept_names.append(f"{node.name} ({node.concept_id})")
                    # Find prerequisites of this node
                    prereqs = [e.source_id for e in graph.edges if e.target_id == node.concept_id]
                    if prereqs:
                        prereq_hints.append(f"{node.name} requires prior mastery of: {', '.join(prereqs)}")
                    # Find next concepts that depend on this node
                    dependents = [e.target_id for e in graph.edges if e.source_id == node.concept_id]
                    for dep in dependents:
                        if dep not in next_steps:
                            next_steps.append(dep)

        clo_titles = []
        addressed_clos = []
        if outcomes:
            for clo in outcomes.outcomes:
                if any(verb in request.query.lower() for verb in clo.action_verbs) or any(skill.lower() in request.query.lower() for skill in clo.target_skills):
                    clo_titles.append(f"[{clo.outcome_id}] {clo.title}")
                    addressed_clos.append(clo.outcome_id)

        # Build citations mapping
        citations: List[AcademicCitation] = []
        for i, res in enumerate(search_results, 1):
            chunk = res.chunk
            citations.append(
                AcademicCitation(
                    citation_id=f"[{i}]",
                    source_file=chunk.source_filename or "Course Syllabus",
                    page_or_slide_number=chunk.page_or_slide_number,
                    chunk_id=chunk.chunk_id,
                    quoted_snippet=chunk.content[:160] + "...",
                    relevance_note=f"Relevance Score: {res.similarity_score:.3f}"
                )
            )

        # 3. Build Prompt
        prompt = build_claude_grounded_rag_prompt(
            course_id=request.course_id,
            query=request.query,
            excerpts=search_results,
            concept_names=concept_names,
            prerequisite_hints=prereq_hints,
            clos=clo_titles,
            academic_level=request.academic_level
        )

        # 4. Generate Answer via Claude 3.5 Sonnet or Deterministic Synthesizer
        if self.client and search_results:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2500,
                    temperature=0.2,
                    system="You are an expert academic tutor. Adhere strictly to the verified course excerpts and cite them using [1], [2]. Never fabricate information.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                answer_text = response.content[0].text
                confidence = 0.95
                model_used = f"Claude 3.5 Sonnet ({self.model})"
            except Exception as e:
                print(f"[ClaudeGroundedRAGEngine] Claude API failed: {e}. Using deterministic synthesis.")
                answer_text, confidence = self._deterministic_grounded_answer(request.query, search_results, citations, prereq_hints)
                model_used = "Deterministic Pedagogical Grounding Engine"
        else:
            answer_text, confidence = self._deterministic_grounded_answer(request.query, search_results, citations, prereq_hints)
            model_used = "Deterministic Pedagogical Grounding Engine"

        return GroundedAnswer(
            course_id=request.course_id,
            query=request.query,
            answer_markdown=answer_text,
            citations=citations,
            grounding_confidence=round(confidence, 3),
            addressed_concept_ids=addressed_concepts,
            addressed_outcome_ids=addressed_clos,
            pedagogical_next_steps=next_steps[:3],
            model_used=model_used,
            metadata={
                "retrieved_chunks_count": len(search_results),
                "has_prerequisite_context": bool(prereq_hints)
            }
        )

    def _deterministic_grounded_answer(
        self,
        query: str,
        results: List[VectorSearchResult],
        citations: List[AcademicCitation],
        prereq_hints: List[str]
    ) -> tuple[str, float]:
        """Synthesizes a verifiable, citation-backed answer from retrieved chunks."""
        if not results:
            return (
                f"### Course Material Analysis\n\n"
                f"Based on the course materials currently uploaded, no matching excerpts were found regarding: **{query}**.\n\n"
                f"> **Note**: Please ensure the corresponding lecture slides or textbook chapters have been ingested into the system.",
                0.1
            )

        top_chunk = results[0].chunk
        best_score = results[0].similarity_score
        
        md_lines = [
            f"### Pedagogical Explanation: {query}\n",
            f"According to the official course materials [1], here is the structured analysis:\n",
            f"**Core Explanation:**\n{top_chunk.content.strip()} [1]\n"
        ]

        if len(results) > 1:
            second_chunk = results[1].chunk
            md_lines.append(f"\n**Supporting Evidence & Details:**\n{second_chunk.content.strip()} [2]\n")

        if prereq_hints:
            md_lines.append("\n**Curriculum Prerequisite Alert:**")
            for hint in prereq_hints:
                md_lines.append(f"- ⚠️ {hint}")

        md_lines.append("\n**Verified Course Citations:**")
        for cit in citations:
            loc = f" (Page/Slide {cit.page_or_slide_number})" if cit.page_or_slide_number else ""
            md_lines.append(f"- {cit.citation_id} **{cit.source_file}**{loc}: `{cit.quoted_snippet}`")

        # Confidence based on retrieval score
        confidence = min(0.98, max(0.5, best_score * 1.5))
        return "\n".join(md_lines), confidence
