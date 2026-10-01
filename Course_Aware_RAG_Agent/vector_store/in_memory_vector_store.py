"""
Course-Aware RAG Agent (AI #1) — In-Memory Vector Store & Cosine Search (Phase 4)
Provides vector indexing, cosine similarity ranking, metadata filtering, and disk persistence.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from Course_Aware_RAG_Agent.models.vector_schemas import (
    CourseChunk,
    VectorSearchResult,
    VectorQueryRequest,
)
from Course_Aware_RAG_Agent.vector_store.openai_embeddings import OpenAIEmbeddingsGenerator


class CourseVectorStore:
    """
    In-memory vector database per course, optimized for dense vector retrieval (1536-dim),
    filtered by academic metadata, with persistent JSON snapshotting.
    """

    def __init__(
        self,
        course_id: str,
        embeddings_generator: Optional[OpenAIEmbeddingsGenerator] = None,
        storage_dir: Optional[Path] = None
    ):
        self.course_id = course_id
        self.embedder = embeddings_generator or OpenAIEmbeddingsGenerator()
        if storage_dir is None:
            self.storage_dir = Path(__file__).resolve().parent.parent / "data" / "vector_indexes"
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.chunks: List[CourseChunk] = []

    def _get_index_file(self) -> Path:
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in self.course_id)
        return self.storage_dir / f"{safe_name}_index.json"

    def add_chunks(self, new_chunks: List[CourseChunk]) -> int:
        """Embeds any un-embedded chunks and indexes them."""
        unembedded = [c for c in new_chunks if not c.embedding]
        if unembedded:
            texts = [c.content for c in unembedded]
            embeddings = self.embedder.embed_texts(texts)
            for chunk, emb in zip(unembedded, embeddings):
                chunk.embedding = emb

        self.chunks.extend(new_chunks)
        self.save_index()
        return len(new_chunks)

    def search(
        self,
        query_text: str,
        top_k: int = 4,
        min_similarity: float = 0.3,
        filter_concept_ids: Optional[List[str]] = None
    ) -> List[VectorSearchResult]:
        """
        Executes Cosine Similarity search over indexed chunks with optional concept filters.
        """
        if not self.chunks:
            return []

        query_vec = self.embedder.embed_query(query_text)
        scored_results: List[VectorSearchResult] = []

        for chunk in self.chunks:
            if not chunk.embedding:
                continue

            # Optional Concept Filtering
            if filter_concept_ids:
                if not any(cid in chunk.linked_concept_ids for cid in filter_concept_ids):
                    continue

            # Dot product (both vectors are L2-normalized unit vectors)
            dot_product = sum(a * b for a, b in zip(query_vec, chunk.embedding))

            if dot_product >= min_similarity:
                # Clamp between -1.0 and 1.0 to ensure validation integrity
                sim = max(-1.0, min(1.0, dot_product))
                scored_results.append(
                    VectorSearchResult(chunk=chunk, similarity_score=round(sim, 4))
                )

        # Sort descending by similarity
        scored_results.sort(key=lambda r: r.similarity_score, reverse=True)
        return scored_results[:top_k]

    def save_index(self) -> Path:
        """Persists indexed chunks and vectors to JSON."""
        file_path = self._get_index_file()
        data = {
            "course_id": self.course_id,
            "total_chunks": len(self.chunks),
            "chunks": [c.model_dump() for c in self.chunks]
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return file_path

    def load_index(self) -> bool:
        """Loads index from disk if present."""
        file_path = self._get_index_file()
        if not file_path.exists():
            return False
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.chunks = [CourseChunk.model_validate(c) for c in data.get("chunks", [])]
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics on the indexed chunks."""
        total_tokens = sum(c.token_count for c in self.chunks)
        modalities = set(c.modality_source.value for c in self.chunks)
        all_concepts = set()
        for c in self.chunks:
            all_concepts.update(c.linked_concept_ids)

        return {
            "course_id": self.course_id,
            "total_chunks": len(self.chunks),
            "total_estimated_tokens": total_tokens,
            "modalities_covered": list(modalities),
            "unique_concepts_tagged": len(all_concepts),
            "vector_dimension": self.embedder.dimensions,
            "embedding_model": self.embedder.model
        }
