from fastapi import FastAPI, HTTPException
from app.api.schemas import QueryRequest, QueryResponse
from app.services.rag_service import RAGService
from app.storage.db import init_db
from app.core.config import settings


app = FastAPI(title="RAG Assistant API")

rag_service = None


@app.on_event("startup")
def startup_event():
    global rag_service
    init_db()
    rag_service = RAGService(pdf_path="data/raw/sf.pdf")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cache")
def cache_stats():
    return {
        "cache_size": rag_service.cache.size()
    }


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = rag_service.answer_query(
        query=request.query ,
        top_k=request.top_k or settings.TOP_K,
        alpha=request.alpha or settings.ALPHA
    )
    return result


