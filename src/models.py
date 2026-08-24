from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class PageDocument:
    source: str
    page: int
    text: str

@dataclass
class Chunk:
    chunk_id: str
    source: str
    page: int
    chunk_index: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class SearchResult:
    chunk: Chunk
    semantic_score: float
    lexical_score: float
    combined_score: float
