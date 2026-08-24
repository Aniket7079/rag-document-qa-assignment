from pathlib import Path

from .config import DATA_DIR, STORAGE_DIR, settings
from .chunk import chunk_pages
from .embeddings import OpenAIEmbedder
from .extract import extract_corpus
from .llm import AnswerGenerator
from .models import Chunk, SearchResult
from .retriever import Retriever
from .vector_store import FAISSStore


class RAGPipeline:
    def __init__(self) -> None:
        self.store = FAISSStore(STORAGE_DIR / "index.faiss", STORAGE_DIR / "metadata.json")
        self.embedder = OpenAIEmbedder()
        self.retriever = Retriever(
            self.store,
            self.embedder,
            settings.top_k,
            settings.retrieval_threshold,
        )
        self.generator = AnswerGenerator()

    def build_index(self) -> tuple[int, int]:
        pages = extract_corpus(DATA_DIR)
        chunks = chunk_pages(pages, settings.chunk_size, settings.chunk_overlap)
        vectors = self.embedder.embed_texts([c.text for c in chunks])
        self.store.build(vectors, chunks)
        return len(pages), len(chunks)

    def load_index(self) -> None:
        self.store.load()

    def query(self, question: str) -> tuple[str, list[SearchResult]]:
        if not self.store.exists:
            self.load_index()
        results = self.retriever.retrieve(question)
        if not self.retriever.is_answerable(results):
            return "I could not find the answer in the provided documents.", results
        return self.generator.answer(question, results), results
