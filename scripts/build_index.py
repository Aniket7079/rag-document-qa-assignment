from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.rag import RAGPipeline

if __name__ == "__main__":
    pipeline = RAGPipeline()
    pages, chunks = pipeline.build_index()
    print(f"Indexed {pages} pages into {chunks} chunks.")
