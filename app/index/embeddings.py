from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name: str = 'intfloat/multilingual-e5-small'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str], batch_size: int = 16, normalize: bool = True) -> np.ndarray:
        if not texts:
            return np.array([],dtype=np.float32)
        
        vectors = self.model.encode(texts, batch_size=batch_size, show_progress_bar=True,
                                    normalize_embeddings=normalize, convert_to_numpy=True)
        
        return vectors.astype(np.float32)
    
    
        
