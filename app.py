import os
import sys
from pathlib import Path 

import streamlit as st 

ROOT = Path(__file__).resolve().parent 
sys.path.insert(0, str(ROOT))

from src.config import DATA_DIR, STORAGE_DIR, settings
from src.rag import RAGPipeline

st.set_page_config(page_title="Atman Cloud - RAG Q&A", page_icon="🔎", layout="wide")

st.title("Atman Cloud - RAG Document Q&A")
st.caption("Ask questions over the provided internal PDF knowledge base.")

with st.sidebar:
    st.subheader("System")
    st.write(f"Embedding: `{settings.embedding_model}`")
    st.write(f"LLM: `{settings.chat_model}`")
    st.write(f"Top K: `{settings.top_k}`")
    st.write(f"Threshold: `{settings.retrieval_threshold}`")
    st.divider()
    st.write(f"Documents: **{len(list(DATA_DIR.glob('*.pdf')))}**")
    st.write(f"Index ready: **{(STORAGE_DIR / 'index.faiss').exists()}**")
    rebuild = st.button("Rebuild index", use_container_width=True)

if rebuild:
    try:
        with st.spinner("Extracting PDFs, chunking text and building FAISS index..."):
            pipeline = RAGPipeline()
            pages, chunks = pipeline.build_index()
        st.success(f"Indexed {pages} pages into {chunks} chunks.")
        st.rerun()
    except Exception as exc:
        st.error(str(exc))

if not (STORAGE_DIR / "index.faiss").exists():
    st.info("No index found. Run `python scripts/build_index.py` or use **Rebuild index** in the sidebar.")
    st.stop()

@st.cache_resource
def get_pipeline() -> RAGPipeline:
    pipeline = RAGPipeline()
    pipeline.load_index()
    return pipeline

pipeline = get_pipeline()
question = st.text_area(
    "Question",
    placeholder="Example: What is the Enterprise uptime guarantee?",
    height=110,
)

if st.button("Ask", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving relevant context and generating answer..."):
            try:
                answer, results = pipeline.query(question.strip())
            except Exception as exc:
                st.error(str(exc))
            else:
                st.subheader("Answer")
                st.write(answer)

                st.subheader("Sources")
                for item in results:
                    c = item.chunk
                    with st.expander(f"{c.source} | page {c.page} | {c.chunk_id} | score {item.combined_score:.3f}"):
                        st.write(c.text)
