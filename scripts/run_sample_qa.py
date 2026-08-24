from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.rag import RAGPipeline

QUESTIONS = [
    "How many PTO days can a full-time employee accrue per year?",
    "How long does a password reset link remain valid?",
    "What is the Standard plan monthly price and included storage?",
    "What is the uptime guarantee for the Enterprise plan?",
    "How long are deleted CloudSync Pro files retained?",
    "What should I do if the CloudSync Pro LED is blinking red?",
    "What is required to access Restricted Data?",
    "How soon before a new employee starts does IT provision email, Slack, and GitHub?",
    "What is the API endpoint for uploading a file?",
    "What happens when the API rate limit is exceeded?",
    "What is Atman Cloud's office address in Mumbai?",
    "Does the company offer a free laptop to every employee?",
]


def main() -> None:
    pipeline = RAGPipeline()
    pipeline.load_index()
    lines = ["# Sample Q&A Log", ""]
    for i, question in enumerate(QUESTIONS, start=1):
        answer, sources = pipeline.query(question)
        lines += [f"## {i}. {question}", "", answer, "", "**Sources**"]
        for item in sources:
            c = item.chunk
            lines.append(
                f"- {c.source} - page {c.page} - chunk {c.chunk_id} - score {item.combined_score:.3f}"
            )
        lines.append("")
    out = ROOT / "sample_qa_runtime.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
