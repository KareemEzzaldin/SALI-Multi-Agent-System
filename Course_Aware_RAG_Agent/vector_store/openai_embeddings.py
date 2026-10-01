"""
Course-Aware RAG Agent (AI #1) — OpenAI Embeddings Generator (Phase 4)
Uses OpenAI's text-embedding-3-small with fallback pseudo-semantic embedding for offline development.
"""
from __future__ import annotations
import hashlib
import math
import os
import re
from typing import List, Optional


class OpenAIEmbeddingsGenerator:
    """
    Generates high-dimensional dense vector embeddings using OpenAI text-embedding-3-small.
    Dimension: 1536 (default) or configurable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.dimensions = dimensions
        self.client = None

        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"[OpenAIEmbeddingsGenerator] Warning: OpenAI client init error: {e}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a batch of text strings into normalized float vectors.
        """
        if not texts:
            return []

        if self.client:
            try:
                # Call OpenAI embeddings API
                response = self.client.embeddings.create(
                    model=self.model,
                    input=texts,
                    dimensions=self.dimensions
                )
                return [data_item.embedding for data_item in response.data]
            except Exception as e:
                print(f"[OpenAIEmbeddingsGenerator] OpenAI API call failed: {e}. Using deterministic semantic fallback.")

        # Deterministic semantic fallback for offline / mock testing
        return [self._fallback_embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query string."""
        return self.embed_texts([text])[0]

    def _fallback_embed(self, text: str) -> List[float]:
        """
        Deterministic pseudo-semantic embedding vector of specified dimensions.
        Computes a normalized n-gram hashed bag-of-words distribution.
        Semantically similar texts will naturally yield high cosine similarity.
        """
        vec = [0.0] * self.dimensions
        words = re.findall(r"\b[A-Za-z0-9_-]+\b", text.lower())

        if not words:
            vec[0] = 1.0
            return vec

        for word in words:
            # Word unigram hash
            h1 = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16) % self.dimensions
            vec[h1] += 1.0

            # Sub-word char trigrams
            for k in range(len(word) - 2):
                tri = word[k:k+3]
                h_tri = int(hashlib.md5(tri.encode("utf-8")).hexdigest(), 16) % self.dimensions
                vec[h_tri] += 0.3

        # L2 Normalization (Unit Length)
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0.0:
            vec = [v / norm for v in vec]

        return vec
