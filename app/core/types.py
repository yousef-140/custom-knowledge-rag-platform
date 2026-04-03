from dataclasses import dataclass

@dataclass
class Page:
    page_number: int
    text: str
    source_path: str
    char_count: int
    is_empty: bool

@dataclass
class Chunk:
    chunk_id: str
    text: str
    source_path: str
    page_start: int
    page_end: int
    char_start: int
    char_end: int
