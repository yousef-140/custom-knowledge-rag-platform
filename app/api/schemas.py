from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    alpha: float = 0.5


class QueryResponse(BaseModel):
    answer: str
    latency: float
    validation: dict
    retrieved_count: int
    cache_hit: bool