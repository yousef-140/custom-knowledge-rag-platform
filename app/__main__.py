from app.ingest.pdf_loader import load_pdf
from app.index.chunking_fixed import chunk_pages_fixed
from app.index.embeddings import Embedder
from app.core.logging import setup_logging
from app.index.faiss_index import FaissIndex
from app.retrieve.retriever import Retriever
from app.retrieve.hybrid import HybridRetriever
from app.retrieve.bm25_search import BM25Search
from app.storage.db import init_db, log_query, log_retrieval
from app.generation.context_compressor import compress_results
from app.generation.llm_client import OllamaClient
from app.generation.validation import validate_answer_format
from app.generation.prompt_builder import build_prompt
import time


def main():
    setup_logging()
    init_db()

    pages = load_pdf("data/raw/sf.pdf")
    chunks = chunk_pages_fixed(pages, chunk_size=800, overlap=150)

    embedder = Embedder()
    texts = [chunk.text for chunk in chunks]
    vectors = embedder.encode(texts)

    dimension = vectors.shape[1]
    index = FaissIndex(dimension, nlist=5)
    index.train(vectors)
    index.add(vectors)

    retriever = Retriever(index, chunks, embedder)
    bm25_search = BM25Search(chunks)
    hybrid = HybridRetriever(retriever, bm25_search)

    query = "what is machine learning"

    start = time.time()

    results = hybrid.search(query, top_k=5, alpha=0.5)
    compressed_results = compress_results(query, results, embedder)

    prompt = build_prompt(query, compressed_results)

    llm = OllamaClient(model_name="llama3.2")
    answer = llm.generate(prompt)

    latency = time.time() - start

    validation = validate_answer_format(answer)

    query_id = log_query(query, answer, latency)
    log_retrieval(query_id, results)

    print("\nVALIDATION:")
    print(validation)

    print("\nFINAL ANSWER:\n")
    print(answer)

    for r in compressed_results[:3]:
        print(f"\noriginal: {r['text'][:300]}")
        print(f"\ncompressed: {r['compressed_text']}")
        print("-" * 30)


if __name__ == "__main__":
    main()


    """
    query
↓
hybrid retrieval
↓
compressed results
↓
build prompt
↓
llm.generate(prompt)
↓
validate answer
↓
log answer + retrieval
"""