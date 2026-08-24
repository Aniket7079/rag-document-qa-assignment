from openai import OpenAI
import numpy as np

from .config import settings


class OpenAIEmbedder:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env before building the index.")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model

    def embed_texts(self, texts: list[str], batch_size: int = 64) -> np.ndarray:
        vectors: list[list[float]] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            response = self.client.embeddings.create(model=self.model, input=batch)
            vectors.extend(item.embedding for item in response.data)
        return np.asarray(vectors, dtype="float32")

    def embed_query(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(model=self.model, input=[text])
        return np.asarray(response.data[0].embedding, dtype="float32")
