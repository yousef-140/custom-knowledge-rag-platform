from app.core.types import Chunk, Page
import hashlib


def _split_text_recursively(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    """
    Recursively split text using a list of separators.
    If no separator works, fall back to fixed slicing.
    """
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    if not separators:
        # fallback: fixed slicing
        chunks = []
        start = 0
        while start < len(text):
            part = text[start:start + chunk_size].strip()
            if part:
                chunks.append(part)
            start += chunk_size
        return chunks

    sep = separators[0]
    parts = text.split(sep)

    if len(parts) == 1:
        return _split_text_recursively(text, chunk_size, separators[1:])

    chunks: list[str] = []
    current = ""

    for part in parts:
        candidate = part if not current else current + sep + part

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current.strip():
                chunks.extend(_split_text_recursively(current, chunk_size, separators[1:]))
            current = part

    if current.strip():
        chunks.extend(_split_text_recursively(current, chunk_size, separators[1:]))

    return chunks


def chunk_pages_recursive(pages: list[Page], chunk_size: int) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    full_text_parts: list[str] = []
    char_to_page: list[int] = []

    for page in pages:
        t = page.text or ""
        full_text_parts.append(t + "\n")
        char_to_page.extend([page.page_number] * (len(t) + 1))

    full_text = "".join(full_text_parts)

    if not full_text.strip():
        return []

    separators = ["\n\n", "\n", ". ", "? ", "! ", " "]
    text_chunks = _split_text_recursively(full_text, chunk_size, separators)

    chunks: list[Chunk] = []
    source_path = pages[0].source_path if pages else "unknown"

    cursor = 0
    for chunk_text in text_chunks:
        start = full_text.find(chunk_text, cursor)
        if start == -1:
            start = cursor
        end = start + len(chunk_text)

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

        cursor = end

    return chunks