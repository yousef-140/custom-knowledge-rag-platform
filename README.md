# Custom Knowledge RAG Platform

A production-style Retrieval-Augmented Generation (RAG) platform for querying custom uploaded knowledge sources.

This project is designed as a strong, reusable MVP that can evolve into a multi-client document intelligence assistant. A client can upload domain-specific documents, and the system retrieves grounded context from those documents before generating answers with citations.

## Overview

The platform supports an end-to-end RAG workflow:

Documents  
→ Ingestion  
→ Cleaning  
→ Chunking  
→ Embeddings  
→ FAISS / BM25  
→ Hybrid Retrieval  
→ Context Selection  
→ Context Compression  
→ Prompt Builder  
→ Local LLM  
→ Answer  
→ Logging / Monitoring

The current version is optimized for a single or small custom document collection and is built with a modular architecture suitable for extension into a reusable client-facing system.

## Features

- PDF ingestion and text extraction
- Text cleaning and metadata handling
- Fixed chunking pipeline
- Sentence-transformer embeddings
- FAISS vector indexing and search
- BM25 lexical retrieval
- Hybrid retrieval (vector + BM25)
- Context selection and context compression
- Local LLM answering via Ollama
- Prompt validation and source formatting
- SQLite logging and lightweight monitoring
- FastAPI API layer
- Simple in-memory query caching
- Retrieval evaluation with Recall@K and MRR
- Failure analysis workflow for debugging retrieval behavior

## Tech Stack

- Python
- FastAPI
- Uvicorn
- sentence-transformers
- FAISS
- rank-bm25
- Ollama
- SQLite
- python-dotenv
- NumPy
- pypdf

## Project Structure

```text
rag-plat/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── eval/
│   ├── generation/
│   ├── index/
│   ├── ingest/
│   ├── retrieve/
│   ├── services/
│   ├── storage/
│   ├── __init__.py
│   └── __main__.py
│
├── data/
│   ├── raw/
│   └── eval/
│
├── tests/
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Architecture

### Retrieval Pipeline

1. Load source documents
2. Extract and clean text
3. Split text into chunks
4. Generate embeddings
5. Build FAISS vector index
6. Build BM25 lexical index
7. Run hybrid retrieval
8. Select and compress context
9. Build grounded prompt
10. Generate answer with a local LLM
11. Validate output format
12. Log queries and retrieval traces

### Answering Pipeline

User Query  
→ Hybrid Retrieval  
→ Top Chunks  
→ Context Selection  
→ Context Compression  
→ Prompt Builder  
→ Ollama LLM  
→ Final Answer with Sources

## API Endpoints

- `GET /health`  
  Health check for the API service

- `POST /query`  
  Query the indexed knowledge source

- `GET /stats`  
  Return simple monitoring statistics

- `GET /cache`  
  Return basic cache stats

## Example Request

### POST `/query`

```json
{
  "query": "what is encapsulation",
  "top_k": 5,
  "alpha": 0.5
}
```

## Example Response

```json
{
  "answer": "Answer:\nEncapsulation is the process of enclosing programming elements to control access and interaction with them.\n\nSources:\n- data/raw/sf.pdf, Page 1",
  "latency": 1.82,
  "validation": {
    "valid": true,
    "reason": "ok"
  },
  "retrieved_count": 5,
  "cache_hit": false
}
```

## Local Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

```bash
ollama serve
```

### 4. Pull a local model

```bash
ollama pull llama3.2
```

### 5. Run the API

```bash
uvicorn app.api.main:app --reload
```

### 6. Open API docs

```text
http://127.0.0.1:8000/docs
```

## Configuration

Environment variables are loaded through `.env`.

Example `.env.example`:

```env
MODEL_NAME=llama3.2
PDF_PATH=data/raw/sf.pdf
TOP_K=5
ALPHA=0.5
MAX_CONTEXT_CHUNKS=3
MAX_CONTEXT_CHARS=2000
TEMPERATURE=0.0
OLLAMA_BASE_URL=http://localhost:11434
```

## Evaluation

The project includes a basic retrieval evaluation workflow using a gold dataset.

Supported retrieval metrics:
- Recall@K
- MRR

It also includes manual failure analysis to classify issues into:
- ingestion / cleaning failure
- chunking failure
- retrieval failure
- ranking failure
- generation / prompt failure

## Monitoring and Logging

SQLite is used to log:
- user queries
- generated answers
- latency
- retrieved chunk IDs
- retrieval rank and scores

This makes the project easier to debug, evaluate, and extend into a more production-ready system.

## Current MVP Scope

This version currently supports a single or small custom document collection and is best described as a production-style MVP.

It is intentionally built with reusable layers so it can evolve into a broader document intelligence platform where:
- clients upload their own sources
- each client has isolated collections
- prompts can be customized per client or use case
- retrieval and generation are grounded in client-specific knowledge

## Future Improvements

- Upload endpoint for client documents
- Multi-document collections
- Per-client prompt customization
- Multi-client / multi-tenant support
- Cross-encoder reranking
- Better PDF text normalization
- Cache invalidation using document hashes
- Dockerized deployment
- Streaming responses
- Authentication and access control
- Admin dashboard for uploads and monitoring

## Suggested Use Cases

- Study assistant for course materials
- Internal company knowledge assistant
- HR policy assistant
- Technical documentation assistant
- Legal/manual/document assistant
- Custom domain QA over uploaded files

## CV / Portfolio Framing

This project demonstrates practical skills in:

- Retrieval-Augmented Generation (RAG)
- Information retrieval
- Semantic search
- Hybrid retrieval systems
- FastAPI backend development
- Local LLM integration
- Evaluation and failure analysis
- Monitoring and caching
- Production-oriented project structure

### Suggested CV Bullet

Built a production-style domain-aware RAG platform for custom document collections using PDF ingestion, sentence-transformer embeddings, FAISS vector search, BM25 lexical retrieval, hybrid ranking, local LLM answering via Ollama, FastAPI serving, SQLite logging, evaluation metrics, and caching.

## Repository Description

Production-style RAG platform for querying custom uploaded knowledge sources using FAISS, BM25, FastAPI, Ollama, SQLite, and hybrid retrieval.

## Suggested GitHub Topics

`rag` `retrieval-augmented-generation` `fastapi` `faiss` `bm25` `ollama` `llm` `nlp` `python` `document-ai`

## License

Add your preferred license before publishing the repository.
