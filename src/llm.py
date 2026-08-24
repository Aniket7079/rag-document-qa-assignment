from openai import OpenAI

from .config import settings
from .models import SearchResult

SYSTEM_PROMPT = """You are a document question-answering assistant.
Answer only from the supplied context. Do not use outside knowledge.
If the context does not contain the answer, say you could not find the answer in the provided documents.
Be concise and precise. Do not invent policies, numbers, endpoints, dates, or product behavior.
"""


def build_context(results: list[SearchResult]) -> str:
    blocks = []
    for item in results:
        c = item.chunk
        blocks.append(
            f"[Source: {c.source} | Page: {c.page} | Chunk: {c.chunk_id}]\n{c.text}"
        )
    return "\n\n---\n\n".join(blocks)


class AnswerGenerator:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env before using the app.")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.chat_model

    def answer(self, question: str, results: list[SearchResult]) -> str:
        context = build_context(results)
        prompt = f"""Question:\n{question}\n\nContext:\n{context}\n\nAnswer the question using only this context."""
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return (response.choices[0].message.content or "").strip()
