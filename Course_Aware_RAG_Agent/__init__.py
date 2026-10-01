"""
Course-Aware RAG Agent (AI #1) Package
Course Intelligence & Grounding Engine for SALI.
"""
from .models.ingestion_schemas import ModalityType, ExtractedSegment, IngestionResponse
from .models.outcomes_schemas import BloomTaxonomyLevel, LearningOutcomeItem, CourseOutcomesManifest, ParseOutcomesRequest
from .models.concept_graph_schemas import (
    ConceptRelationType,
    ConceptDifficulty,
    ConceptNode,
    ConceptEdge,
    CourseConceptGraph,
    BuildConceptGraphRequest,
)
from .models.vector_schemas import (
    ChunkingConfig,
    CourseChunk,
    VectorSearchResult,
    VectorQueryRequest,
    IndexCourseContentRequest,
)
from .models.rag_schemas import (
    AcademicCitation,
    GroundedAnswer,
    CourseRAGQueryRequest,
)
from .parsers.pdf_parser import PDFParser
from .parsers.pptx_parser import PPTXParser
from .multimodal.gemini_ingestion import GeminiMultimodalProcessor
from .outcomes.outcomes_parser import ClaudeOutcomesParser, build_claude_outcomes_prompt
from .outcomes.storage import OutcomesStorage
from .concept_graph.dag_engine import DAGEngine
from .concept_graph.graph_extractor import ClaudeConceptGraphExtractor, build_claude_concept_graph_prompt
from .concept_graph.storage import ConceptGraphStorage
from .vector_store.pedagogical_chunker import PedagogicalChunker
from .vector_store.openai_embeddings import OpenAIEmbeddingsGenerator
from .vector_store.in_memory_vector_store import CourseVectorStore
from .rag.grounded_rag_engine import ClaudeGroundedRAGEngine, build_claude_grounded_rag_prompt
from .api.upload_routes import router as ingestion_router
from .api.outcomes_routes import router as outcomes_router
from .api.graph_routes import router as graph_router
from .api.vector_routes import router as vector_router
from .api.rag_routes import router as rag_router

__all__ = [
    "ModalityType",
    "ExtractedSegment",
    "IngestionResponse",
    "BloomTaxonomyLevel",
    "LearningOutcomeItem",
    "CourseOutcomesManifest",
    "ParseOutcomesRequest",
    "ConceptRelationType",
    "ConceptDifficulty",
    "ConceptNode",
    "ConceptEdge",
    "CourseConceptGraph",
    "BuildConceptGraphRequest",
    "ChunkingConfig",
    "CourseChunk",
    "VectorSearchResult",
    "VectorQueryRequest",
    "IndexCourseContentRequest",
    "AcademicCitation",
    "GroundedAnswer",
    "CourseRAGQueryRequest",
    "PDFParser",
    "PPTXParser",
    "GeminiMultimodalProcessor",
    "ClaudeOutcomesParser",
    "build_claude_outcomes_prompt",
    "OutcomesStorage",
    "DAGEngine",
    "ClaudeConceptGraphExtractor",
    "build_claude_concept_graph_prompt",
    "ConceptGraphStorage",
    "PedagogicalChunker",
    "OpenAIEmbeddingsGenerator",
    "CourseVectorStore",
    "ClaudeGroundedRAGEngine",
    "build_claude_grounded_rag_prompt",
    "ingestion_router",
    "outcomes_router",
    "graph_router",
    "vector_router",
    "rag_router",
]




