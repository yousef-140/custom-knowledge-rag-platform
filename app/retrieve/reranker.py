from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, results, top_k=5):

        pairs = [(query, r["text"]) for r in results]

        scores = self.model.predict(pairs)

        for r, s in zip(results, scores):
            r["rerank_score"] = float(s)

        results.sort(key=lambda x: x["rerank_score"], reverse=True)

        return results[:top_k]
