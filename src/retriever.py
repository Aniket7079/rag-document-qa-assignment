import re
from collections import Counter

from .embeddings import OpenAIEmbedder
from .models import SearchResult
from .vector_store import FAISSStore


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _lexical_score(query: str, text: str) -> float:
    q = Counter(_tokens(query))
    d = Counter(_tokens(text))
    if not q:
        return 0.0
    overlap = sum(min(q[t], d[t]) for t in q)
    return overlap / sum(q.values())


class Retriever:
    def __init__(self, store: FAISSStore, embedder: OpenAIEmbedder, top_k: int, threshold: float) -> None:
        self.store = store
        self.embedder = embedder
        self.top_k = top_k
        self.threshold = threshold

    def retrieve(self, question: str) -> list[SearchResult]:
        query_vector = self.embedder.embed_query(question)
        candidates = self.store.search(query_vector, max(self.top_k * 3, 10))
        results: list[SearchResult] = []
        for idx, semantic in candidates:
            chunk = self.store.chunks[idx]
            lexical = _lexical_score(question, chunk.text)
            combined = 0.75 * semantic + 0.25 * lexical
            results.append(SearchResult(chunk, semantic, lexical, combined))
        results.sort(key=lambda x: x.combined_score, reverse=True)
        return results[:self.top_k]

    def is_answerable(self, results: list[SearchResult]) -> bool:
        return bool(results) and results[0].combined_score >= self.threshold
