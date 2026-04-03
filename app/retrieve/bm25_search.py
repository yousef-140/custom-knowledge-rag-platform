from rank_bm25 import BM25Okapi


class BM25Search:

    def __init__(self, chunks):

        self.chunks = chunks

        corpus = [chunk.text.split() for chunk in chunks]

        self.bm25 = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 5):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for idx, score in ranked[:top_k]:

            chunk = self.chunks[idx]

            results.append({
                "chunk_id":chunk.chunk_id,
                "score": score,
                "text": chunk.text,
                "page_start": chunk.page_start,
                "source": chunk.source_path
            })

        return results