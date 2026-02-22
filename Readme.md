# Project README

This is a Python project with three Python files representing different phases of the project. Below are the instructions for setting up the environment and running the project.

---

## Table of Contents
1. [Environment Setup](#environment-setup)
    - [Using Pipenv](#using-pipenv)
    - [Using Conda](#using-conda)
    - [Using Pip](#using-pip)
2. [Running the Project](#running-the-project)

---

## Environment Setup

### Using Pipenv
Pipenv is a tool that manages dependencies and virtual environments for Python projects.

1. Install Pipenv if you don't have it:
    ```
    pip install pipenv
    ```

2. Navigate to the project directory and create a virtual environment:
    ```
    pipenv install
    ```

3. Activate the virtual environment:
    ```
    pipenv shell
    ```

4. (Optional) Install any additional dependencies:
    ```
    pipenv install <package_name>
    ```

## AI Lawyer — RAG demo with DeepSeek/Groq (Streamlit)

This repository contains a small Retrieval-Augmented Generation (RAG) demo app built with Streamlit that:

- Accepts a PDF upload.
- Splits the document into chunks.
- Stores/retrieves embeddings in a FAISS vector store.
- Uses a Groq-hosted DeepSeek LLM (via LangChain integrations) to answer user questions from retrieved context.

The app is intended as a minimal end-to-end reference for building a document Q&A (AI Lawyer) system using local vector stores and an external LLM provider.

## Key features

- Streamlit UI for quick iteration and testing (`main.py`).
- Modular RAG pipeline (`rag_pipeline.py`, `vector_database.py`).
- FAISS-based persistent vectorstore at `vectorstore/db_faiss`.
- PDF ingestion via `pdfplumber`.
- Example PDFs included in `pdfs/` for quick testing.

## Quick start (3 steps)

1. Create / activate a Python environment (examples below).
2. Install dependencies.
3. Run the Streamlit app.

### Quick commands (macOS / zsh)

If you want to use the repository's included virtualenv, start Streamlit using the bundled binary (example path shown in this repo):

```bash
# Start app using the repo env's streamlit (adjust path if different)
/path/to/repo/env/bin/streamlit run /path/to/repo/main.py
```

Or with a fresh venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_api_key_here"
streamlit run main.py
```

Note: the app now loads uploaded PDFs into `pdfs/` (the directory is auto-created).

## Environment & prerequisites

- Python 3.10+ (project was installed and tested with 3.13 in the included env).
- A valid GROQ API key (if you want to use the Groq DeepSeek model). Set it in your shell or in a `.env` file as `GROQ_API_KEY`.
- Optional: Ollama or other local LLMs if you adapt the code for alternate backends.

Environment variables

- `GROQ_API_KEY` — required to call Groq LLM through the langchain_groq integration. If this is not set, the app will show a helpful message when you attempt to ask a question.

If you have a `.env` file, you can load it before running Streamlit, or I can add automatic `.env` loading upon request.

## How the app works (high level)

1. User uploads a PDF in the Streamlit UI (`main.py`).
2. The PDF is saved to `pdfs/` and loaded using `PDFPlumberLoader`.
3. Text is chunked with `RecursiveCharacterTextSplitter`.
4. Chunks are embedded using `OllamaEmbeddings` (configurable) and stored in a local FAISS database (`vectorstore/db_faiss`).
5. On a user query, the vectorstore performs a similarity search; the resulting documents are combined into a context string.
6. A ChatGroq LLM (Groq) is invoked with a small prompt template to answer based only on the provided context.

## Files & structure

- `main.py` — Streamlit app (UI + orchestrates upload, indexing, retrieval, and query).
- `frontend.py` — alternate frontend/prototype of the chat flow.
- `rag_pipeline.py` — helper functions for retrieval and answering queries (now uses lazy LLM initialization).
- `vector_database.py` — FAISS wrapper used by the app (persist/load vectorstore).
- `pdfs/` — sample PDFs and where uploaded PDFs are stored (auto-created by the app).
- `vectorstore/db_faiss/` — FAISS index files persisted by the app.
- `requirements.txt` / `Pipfile` — dependency manifests.

## Running the app — detailed

1. Install dependencies (recommended inside a venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Export your GROQ API key (or add to a `.env` file):

```bash
export GROQ_API_KEY="gsk_xxx_your_key"
```

3. Run Streamlit:

```bash
streamlit run main.py
```

Open http://localhost:8501 in your browser.

Usage notes

- Use the file uploader to upload a PDF. The app will save it to `pdfs/` and index it.
- Enter a question in the text area and click "Ask AI Lawyer". The app will retrieve the most relevant chunks and ask the Groq model to answer.

## Troubleshooting

- Problem: "The api_key client option must be set..." — set `GROQ_API_KEY` in your environment before starting the app.
- Problem: FileNotFoundError writing to `pdfs/...` — fixed in the code; the app will create `pdfs/` automatically. If you still see permission errors, ensure the repo directory is writable.
- Problem: FAISS load/save issues — ensure `vectorstore/db_faiss` exists and is writable. `main.py` attempts to create it automatically when saving.
- Problem: Streamlit crashes on import due to LLM initialization — this repo now lazily initializes the ChatGroq model; you will get a Streamlit-visible message if the Groq client fails to initialize.

If you still hit a traceback, copy the full traceback text and paste it into an issue or here — I can help debug the exact error.

## Development notes & extension ideas

- Add `.env` auto-loading: load environment variables from `.env` using `python-dotenv` at app startup to make local development smoother (I can add this).
- Add a selectable LLM backend in the UI (Groq, Ollama, local model) and failover strategy.
- Add caching for embeddings and incremental indexing for large corpora.
- Add unit tests for the pipeline (embedding -> faiss -> retrieval -> llm call) and a small integration test with a synthetic document.

## Security & data handling

- Be careful with private PDFs — uploaded files are saved to disk under `pdfs/`. If you deploy this, use secure storage and remove files when done.
- API keys (like `GROQ_API_KEY`) should not be committed to version control. Add `.env` (and `env/`) to `.gitignore`.

## Contribution & support

If you'd like me to make any of the development improvements above (auto `.env` loading, demo mode, LLM backend toggle), tell me which one and I'll implement it and validate by running the app locally.

## License & attribution

This repo contains third-party dependencies (LangChain, Groq, FAISS, Streamlit). Check each dependency's license when you adapt this project for commercial use.

---

If you want, I can now:

- Add automatic `.env` loading so your contained `.env` (if present) is used at startup, or
- Add a small demo/“try without API key” fallback mode, or
- Wire up a simple unit test that indexes a bundled PDF and runs a sample query.

Tell me which you'd like and I’ll apply it now.
