"""
Course-Aware RAG Agent (AI #1) — Vector Chunking & Embeddings Module (Phase 4)
"""
from .pedagogical_chunker import PedagogicalChunker
from .openai_embeddings import OpenAIEmbeddingsGenerator
from .in_memory_vector_store import CourseVectorStore

__all__ = [
    "PedagogicalChunker",
    "OpenAIEmbeddingsGenerator",
    "CourseVectorStore",
]
