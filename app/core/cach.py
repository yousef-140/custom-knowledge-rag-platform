import hashlib
import json


def make_cache_key(query: str, top_k: int, alpha: float, pdf_path: str) -> str:
    raw = json.dumps(
        {
            "query": query.strip().lower(),
            "top_k": top_k,
            "alpha": alpha,
            "pdf_path": pdf_path,
        },
        sort_keys=True
    )
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

class SimpleCache:
    def __init__(self, max_size: int = 100):
        self.store = {}
        self.max_size = max_size

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value):
        if len(self.store) >= self.max_size:
            self.store.clear()
        self.store[key] = value
