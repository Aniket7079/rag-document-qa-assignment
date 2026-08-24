import json
from pathlib import Path
import faiss
import numpy as np

from .models import Chunk


class FAISSStore:
    def __init__(self, index_path: Path, metadata_path: Path) -> None:
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index: faiss.Index | None = None
        self.chunks: list[Chunk] = []

    @property
    def exists(self) -> bool:
        return self.index_path.exists() and self.metadata_path.exists()

    def build(self, vectors: np.ndarray, chunks: list[Chunk]) -> None:
        matrix = vectors.astype("float32")
        faiss.normalize_L2(matrix)
        self.index = faiss.IndexFlatIP(matrix.shape[1])
        self.index.add(matrix)
        self.chunks = chunks
        self.save()

    def save(self) -> None:
        if self.index is None:
            raise RuntimeError("Index has not been built")
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(
            json.dumps([chunk.to_dict() for chunk in self.chunks], indent=2),
            encoding="utf-8",
        )

    def load(self) -> None:
        if not self.exists:
            raise FileNotFoundError("Vector index not found. Run scripts/build_index.py first.")
        self.index = faiss.read_index(str(self.index_path))
        data = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        self.chunks = [Chunk(**item) for item in data]

    def search(self, query_vector: np.ndarray, top_k: int) -> list[tuple[int, float]]:
        if self.index is None:
            self.load()
        vector = query_vector.reshape(1, -1).astype("float32")
        faiss.normalize_L2(vector)
        scores, ids = self.index.search(vector, top_k)
        return [(int(idx), float(score)) for idx, score in zip(ids[0], scores[0]) if idx >= 0]
