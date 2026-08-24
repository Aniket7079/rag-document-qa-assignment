# RAG-Based Document Q&A System

## Overview

This project implements a complete Retrieval-Augmented Generation (RAG) pipeline over the seven PDF documents supplied for the screening assignment.

**Pipeline:**

`PDFs -> Text extraction -> Chunking -> OpenAI embeddings -> FAISS vector store -> Hybrid retrieval -> Grounding check -> LLM answer -> Source display`

The reviewer interacts with the system through a small Streamlit UI.

## Project structure

```text
rag-document-qa/
|-- app.py
|-- README.md
|-- requirements.txt
|-- .env.example
|-- data/
|   |-- API_Reference.pdf
|   |-- Employee_Handbook.pdf
|   |-- FAQ_Support.pdf
|   |-- Onboarding_Guide.pdf
|   |-- Pricing_and_SLA.pdf
|   |-- Product_Manual.pdf
|   `-- Security_Policy.pdf
|-- scripts/
|   |-- build_index.py
|   `-- run_sample_qa.py
|-- src/
|   |-- chunk.py
|   |-- config.py
|   |-- embeddings.py
|   |-- extract.py
|   |-- llm.py
|   |-- models.py
|   |-- rag.py
|   |-- retriever.py
|   `-- vector_store.py
|-- storage/
|   `-- generated index files
|-- tests/
|   |-- test_chunking.py
|   `-- test_extraction.py
`-- sample_qa.md
```

## Design decisions

### 1. PDF extraction

PyMuPDF is used for page-aware extraction. Text blocks are ordered top-to-bottom and left-to-right before joining. This keeps headings, paragraphs, endpoint examples, and table text reasonably ordered for the supplied PDFs.

The extracted object keeps the original document name and page number so every retrieved chunk can be traced back to the source PDF.

### 2. Chunking

The default chunk size is **1200 characters** with **150 characters overlap**.

The splitter first keeps paragraph boundaries. Only unusually long paragraphs are split further. The supplied documents are short and structured, so this keeps related policy/table content together while still producing retrieval-sized passages.

The overlap reduces the chance of losing meaning when a sentence or small table description crosses a chunk boundary.

### 3. Embeddings

The project uses OpenAI `text-embedding-3-small` by default. It gives compact, high-quality text embeddings and keeps setup simple for a reviewer.

The embedding model is configured through `.env`, so it can be changed without editing the source code.

### 4. Vector store

FAISS is used with a normalized inner-product index. After normalization, inner product is cosine similarity, which is a good fit for semantic text search.

The local vector index is stored in `storage/index.faiss`, while source metadata is stored in `storage/metadata.json`.

### 5. Retrieval

Retrieval combines two signals:

- **Semantic similarity (75%)** from FAISS.
- **Token overlap (25%)** as a lightweight lexical signal.

This hybrid score helps when the question contains exact terms such as endpoint names, plan names, policy labels, or error codes.

The top results are sorted by the combined score and the top **5** are passed to the LLM.

### 6. Grounding and unanswerable questions

A retrieval threshold is applied before calling the LLM. When the best result is below the threshold, the system returns:

> I could not find the answer in the provided documents.

The LLM is also prompted to answer only from the retrieved context and to abstain rather than invent missing information.

### 7. Source attribution

Every retrieved chunk carries:

- source document name
- page number
- chunk ID
- retrieval score

The UI displays these source details below the answer so a reviewer can verify the response against the original PDFs.

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Python 3.10 or 3.11 is recommended.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=your_real_key
```

Do not commit `.env`.

### 4. Build the vector index

```bash
python scripts/build_index.py
```

Expected output is similar to:

```text
Indexed 20 pages into XX chunks.
```

The exact chunk count can change if chunk settings are adjusted.

### 5. Start the demo

```bash
streamlit run app.py
```

The browser will open the local Streamlit page. Enter a question and click **Ask**.

## Example questions

Try questions such as:

- How many PTO days can a full-time employee accrue per year?
- What is the Standard plan monthly price?
- What is the Enterprise uptime guarantee?
- What is the upload endpoint?
- What should I do if the LED is blinking red?
- What is required to access Restricted Data?

Also test out-of-scope questions, such as:

- What is the office address in Mumbai?
- Do employees get a free laptop?

The expected behavior for missing answers is to abstain instead of fabricating a response.

## Rebuild from the UI

The Streamlit sidebar has a **Rebuild index** button. Use it after adding or changing PDFs in `data/`.

## Sample Q&A

`sample_qa.md` contains 12 representative questions, including two intentionally unanswerable examples. `scripts/run_sample_qa.py` can generate a fresh runtime log after the index has been built.

```bash
python scripts/run_sample_qa.py
```

This creates `sample_qa_runtime.md`.

## Testing

Run:

```bash
pytest -q
```

The tests cover PDF extraction and the chunking behavior.

## Trade-offs and limitations

- The first index build depends on the selected embedding API and internet access.
- The current chunking strategy is intentionally simple and page-aware. A production system could add layout-aware table parsing and section-aware splitting.
- The lexical component is lightweight rather than a full BM25 implementation.
- The current application does not keep conversation history between questions.
- Retrieval quality depends on the selected embedding model and threshold. In a larger production corpus, I would add a labeled evaluation set and tune the threshold with precision/recall measurements.
- For scanned PDFs, an OCR stage would be needed before chunking.

## AI assistance disclosure

AI coding assistants were used for implementation support and review. The project structure, retrieval behavior, grounding logic, and documentation were reviewed against the assignment requirements and the supplied PDF corpus.

## Submission checklist

- [ ] Push the project to GitHub.
- [ ] Keep `.env` out of Git.
- [ ] Include the seven supplied PDFs in `data/`.
- [ ] Verify `pytest -q` passes.
- [ ] Run the Streamlit demo locally.
- [ ] Test both answerable and unanswerable questions.
- [ ] Share the GitHub repository link.
