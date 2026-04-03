import faiss
import numpy as np


class FaissIndex:

    def __init__(self, dimension: int, nlist: int = 100):
        self.dimension = dimension
        self.nlist = nlist

        quantizer = faiss.IndexFlatIP(dimension)

        self.index = faiss.IndexIVFFlat(
            quantizer,
            dimension,
            nlist,
            faiss.METRIC_INNER_PRODUCT
        )

    def train(self, vectors: np.ndarray):
        if not self.index.is_trained:
            self.index.train(vectors)

    def add(self, vectors: np.ndarray):
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)

        self.index.add(vectors)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        if query_vector.dtype != np.float32:
            query_vector = query_vector.astype(np.float32)

        scores, indices = self.index.search(query_vector, top_k)

        return scores, indices