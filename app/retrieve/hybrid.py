from app.retrieve.retriever import Retriever
from app.retrieve.bm25_search import BM25Search


class HybridRetriever:
    def __init__(self, vector_retriever: Retriever, bm25_search: BM25Search):
        self.vector_retriever = vector_retriever
        self.bm25_search = bm25_search

    def search(self, query: str, top_k: int = 5, alpha: float = 0.5):
        """
        alpha:
            1.0 => vector only
            0.0 => bm25 only
        """

        vector_results = self.vector_retriever.search(query, top_k=top_k * 2)
        bm25_results = self.bm25_search.search(query, top_k=top_k * 2)

        combined = {}

        # normalize vector scores
        if vector_results:
            max_vec = max(r["score"] for r in vector_results) or 1.0
        else:
            max_vec = 1.0

        for r in vector_results:
            key = (r["source"], r["page_start"], r["text"])
            norm_score = r["score"] / max_vec
            combined[key] = {
                **r,
                "vector_score": norm_score,
                "bm25_score": 0.0,
            }

        # normalize bm25 scores
        if bm25_results:
            max_bm25 = max(r["score"] for r in bm25_results) or 1.0
        else:
            max_bm25 = 1.0

        for r in bm25_results:
            key = (r["source"], r["page_start"], r["text"])
            norm_score = r["score"] / max_bm25

            if key in combined:
                combined[key]["bm25_score"] = norm_score
            else:
                combined[key] = {
                    **r,
                    "vector_score": 0.0,
                    "bm25_score": norm_score,
                }

        final_results = []
        for item in combined.values():
            hybrid_score = alpha * item["vector_score"] + (1 - alpha) * item["bm25_score"]
            item["hybrid_score"] = hybrid_score
            final_results.append(item)

        final_results.sort(key=lambda x: x["hybrid_score"], reverse=True)

        return final_results[:top_k]