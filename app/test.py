from app.ingest.pdf_loader import load_pdf
from app.index.chunking_fixed import chunk_pages_fixed
from app.index.chunking_recursive import chunk_pages_recursive
from app.index.embeddings import Embedder
from app.core.logging import setup_logging
from app.index.faiss_index import FaissIndex
from app.index.store import save_index, load_index
from app.generation.context_selector import select_context
from app.generation.prompt_builder import build_prompt
from app.retrieve.hybrid import HybridRetriever
from app.retrieve.retriever import Retriever
from app.retrieve.bm25_search import BM25Search
from app.core.guardrails import filter_safe_context

pages = load_pdf("data/raw/sf.pdf")
chunks = chunk_pages_fixed(pages, chunk_size=800, overlap=150)


embedder = Embedder()

texts = [chunk.text for chunk in chunks]

vectors = embedder.encode(texts)
dimension = vectors.shape[1]

index = FaissIndex(dimension, nlist=5)

index.train(vectors)

index.add(vectors)

query = "what is encapsulation"

query_vec = embedder.encode([query])


scores, ids = index.search(query_vec, top_k=3)
 


retriever = Retriever(index, chunks, embedder)
bm_25search = BM25Search(chunks)
hybrid = HybridRetriever(retriever, bm_25search)

retrieved = hybrid.search(query="What is encapsulation?", top_k=10, alpha=0.5)
selected = select_context(retrieved, max_chunks=3, max_total_chars=2000)
safe_selected = filter_safe_context(selected)
prompt = build_prompt("What is encapsulation?", safe_selected)

print(prompt)