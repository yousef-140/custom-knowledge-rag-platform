import hashlib
from app.core.types import Chunk, Page


def chunk_pages_fixed(pages: list[Page], chunk_size: int, overlap: int) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    # 1) Build one full text + char->page map
    full_text_parts: list[str] = []
    char_to_page: list[int] = []  # maps each character position to a page_number

    for page in pages:
        t = page.text or ""
        full_text_parts.append(t + "\n")
        # +1 for the added "\n"
        char_to_page.extend([page.page_number] * (len(t) + 1))

    full_text = "".join(full_text_parts)

    # edge case: empty document
    if not full_text.strip():
        return []

    # 2) Slice into chunks
    stride = chunk_size - overlap
    chunks: list[Chunk] = []

    source_path = pages[0].source_path if pages else "unknown"

    for start in range(0, len(full_text), stride):
        end = min(start + chunk_size, len(full_text))
        chunk_text = full_text[start:end].strip()

        if not chunk_text:
            if end == len(full_text):
                break
            continue

        # map char positions to page ranges
        page_start = char_to_page[start] if start < len(char_to_page) else char_to_page[-1]
        page_end = char_to_page[end - 1] if (end - 1) < len(char_to_page) else char_to_page[-1]

        chunk_id = hashlib.md5(chunk_text.encode("utf-8")).hexdigest()

        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                text=chunk_text,
                source_path=source_path,
                page_start=page_start,
                page_end=page_end,
                char_start=start,
                char_end=end,
            )
        )

        if end == len(full_text):
            break

    return chunks