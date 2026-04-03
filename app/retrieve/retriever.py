from app.index.embeddings import Embedder
from app.index.faiss_index import FaissIndex


class Retriever:

    def __init__(self, index: FaissIndex, chunks, embedder: Embedder):
        self.index = index
        self.chunks = chunks
        self.embedder = embedder

    def search(self, query: str, top_k: int = 5):

        query_vector = self.embedder.encode([query])

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx < 0:
                continue

            chunk = self.chunks[idx]

            results.append({
                "chunk_id": chunk.chunk_id,
                "score": float(score),
                "text": chunk.text,
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "source": chunk.source_path
            })

        return results