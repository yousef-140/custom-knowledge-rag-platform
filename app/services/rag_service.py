import time
from app.ingest.pdf_loader import load_pdf
from app.index.chunking_fixed import chunk_pages_fixed
from app.index.embeddings import Embedder
from app.index.faiss_index import FaissIndex
from app.retrieve.retriever import Retriever
from app.retrieve.hybrid import HybridRetriever
from app.retrieve.bm25_search import BM25Search
from app.generation.context_compressor import compress_results
from app.generation.context_selector import select_context
from app.generation.prompt_builder import build_prompt
from app.generation.llm_client import OllamaClient
from app.generation.validation import validate_answer_format
from app.storage.db import log_query, log_retrieval
from app.core.config import settings
from app.core.cach import SimpleCache,make_cache_key



class RAGService:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

        pages = load_pdf(settings.PDF_PATH)
        chunks = chunk_pages_fixed(pages, chunk_size=800, overlap=150)

        self.chunks = chunks
        self.embedder = Embedder()

        texts = [chunk.text for chunk in chunks]
        vectors = self.embedder.encode(texts)

        dimension = vectors.shape[1]
        self.index = FaissIndex(dimension, nlist=5)
        self.index.train(vectors)
        self.index.add(vectors)

        self.retriever = Retriever(self.index, self.chunks, self.embedder)
        self.bm25_search = BM25Search(self.chunks)
        self.hybrid = HybridRetriever(self.retriever, self.bm25_search)

        self.llm = OllamaClient(model_name = settings.MODEL_NAME)

def answer_query(self, query: str, top_k: int = 5, alpha: float = 0.5):
    cache_key = make_cache_key(query, top_k, alpha, self.pdf_path)

    cached = self.cache.get(cache_key)
    if cached is not None:
        cached_result = dict(cached)
        cached_result["cache_hit"] = True
        return cached_result

    start = time.time()

    results = self.hybrid.search(query, top_k=top_k, alpha=alpha)
    selected = select_context(results, max_chunks=3, max_total_chars=2000)
    compressed = compress_results(query, selected, self.embedder, max_sentences=2)

    prompt = build_prompt(query, compressed)
    answer = self.llm.generate(prompt)

    latency = time.time() - start
    validation = validate_answer_format(answer)

    query_id = log_query(query, answer, latency)
    log_retrieval(query_id, results)

    result = {
        "answer": answer,
        "latency": latency,
        "validation": validation,
        "retrieved_count": len(results),
        "cache_hit": False,
    }

    self.cache.set(cache_key, result)

    return result