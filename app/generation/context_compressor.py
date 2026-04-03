import re
import numpy as np
from app.index.embeddings import Embedder

def split_sentences(text: str) -> list[str]:

    parts = re.split(r'\n+|(?<=[.!?])\s+', text)

    sentences = []

    for p in parts:
        p = p.strip()

        # ignore very short lines
        if len(p) < 40:
            continue

        sentences.append(p)

    return sentences

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def compress_chunk(query: str, chunk_text: str, embedder: Embedder, max_sentences: int = 2) -> str:
    sentences = split_sentences(chunk_text)

    if not sentences:
        return ""

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    query_vec = embedder.encode([query], batch_size=1, normalize=True)[0]
    sent_vecs = embedder.encode(sentences, batch_size=16, normalize=True)

    scored = []
    for sent, vec in zip(sentences, sent_vecs):
        score = cosine_similarity(query_vec, vec)
        scored.append((sent, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    top_sentences = [s for s, _ in scored[:max_sentences]]

    # optional: preserve original order in text
    ordered = [s for s in sentences if s in top_sentences]

    return " ".join(ordered)


def compress_results(query: str, results: list[dict], embedder: Embedder, max_sentences: int = 2) -> list[dict]:
    compressed_results = []

    for r in results:
        compressed_text = compress_chunk(
            query=query,
            chunk_text=r["text"],
            embedder=embedder,
            max_sentences=max_sentences
        )

        new_item = dict(r)
        new_item["compressed_text"] = compressed_text
        compressed_results.append(new_item)

    return compressed_results