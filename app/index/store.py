import faiss


def save_index(index, path: str):
    faiss.write_index(index, path)


def load_index(path: str):
    return faiss.read_index(path)