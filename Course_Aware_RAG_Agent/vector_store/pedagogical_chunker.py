"""
Course-Aware RAG Agent (AI #1) — Pedagogical Chunker (Phase 4)
Chunks course materials respecting paragraph/sentence boundaries and linking concept metadata.
"""
from __future__ import annotations
import re
from typing import List, Optional, Dict, Any

from Course_Aware_RAG_Agent.models.ingestion_schemas import ModalityType
from Course_Aware_RAG_Agent.models.vector_schemas import CourseChunk, ChunkingConfig
from Course_Aware_RAG_Agent.models.concept_graph_schemas import CourseConceptGraph


class PedagogicalChunker:
    """
    Intelligent text chunker that preserves semantic context,
    maintains slide/page boundaries, and tags chunks with relevant course concepts.
    """

    def __init__(self, config: Optional[ChunkingConfig] = None):
        self.config = config or ChunkingConfig()

    def estimate_tokens(self, text: str) -> int:
        """Approximates token count (avg 4 characters per token)."""
        words = len(text.split())
        return max(1, int(words * 1.3))

    def chunk_content(
        self,
        course_id: str,
        content: str,
        source_filename: Optional[str] = None,
        page_or_slide_number: Optional[int] = None,
        modality_source: ModalityType = ModalityType.TEXT,
        concept_graph: Optional[CourseConceptGraph] = None
    ) -> List[CourseChunk]:
        """
        Splits a content block into overlapping semantic chunks with pedagogical metadata.
        """
        if not content.strip():
            return []

        # Split into paragraphs or sentences
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
        if not paragraphs:
            paragraphs = [content.strip()]

        raw_chunks: List[str] = []
        current_chunk_paragraphs: List[str] = []
        current_token_count = 0
        target_tokens = self.config.chunk_size_tokens
        overlap_tokens = self.config.chunk_overlap_tokens

        for p in paragraphs:
            p_tokens = self.estimate_tokens(p)
            if current_token_count + p_tokens > target_tokens and current_chunk_paragraphs:
                # Flush current chunk
                raw_chunks.append("\n\n".join(current_chunk_paragraphs))
                # Retain last paragraph for overlap if applicable
                if overlap_tokens > 0 and len(current_chunk_paragraphs) > 1:
                    last_p = current_chunk_paragraphs[-1]
                    current_chunk_paragraphs = [last_p, p]
                    current_token_count = self.estimate_tokens(last_p) + p_tokens
                else:
                    current_chunk_paragraphs = [p]
                    current_token_count = p_tokens
            else:
                current_chunk_paragraphs.append(p)
                current_token_count += p_tokens

        if current_chunk_paragraphs:
            raw_chunks.append("\n\n".join(current_chunk_paragraphs))

        # Build CourseChunk objects with concept metadata linkage
        course_chunks: List[CourseChunk] = []
        for i, text in enumerate(raw_chunks, 1):
            chunk_tokens = self.estimate_tokens(text)
            
            # Detect concepts mentioned in this chunk
            linked_concepts = []
            if concept_graph and concept_graph.nodes:
                text_lower = text.lower()
                for node in concept_graph.nodes:
                    node_name_clean = node.name.lower()
                    if node_name_clean in text_lower or any(term.lower() in text_lower for term in node.key_terms):
                        linked_concepts.append(node.concept_id)

            prefix_source = f"{source_filename}_" if source_filename else ""
            slide_suffix = f"p{page_or_slide_number}_" if page_or_slide_number else ""
            chunk_id = f"CHK-{course_id}-{prefix_source}{slide_suffix}{i:03d}"

            course_chunks.append(
                CourseChunk(
                    chunk_id=chunk_id,
                    course_id=course_id,
                    content=text,
                    modality_source=modality_source,
                    source_filename=source_filename,
                    page_or_slide_number=page_or_slide_number,
                    token_count=chunk_tokens,
                    linked_concept_ids=linked_concepts,
                    linked_outcome_ids=[],
                    metadata={
                        "chunk_index": i,
                        "total_chunks_in_block": len(raw_chunks),
                    }
                )
            )

        return course_chunks
