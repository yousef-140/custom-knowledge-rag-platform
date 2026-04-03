def select_context(results , max_chunks = 4 ,max_total_chars = 3000):
    """
    Selects the most relevant chunks of text based on the search results, ensuring that the total number of characters does not exceed a specified limit."""

    selected =[]
    total_chars = 0
    seen_texts = set()

    for r in results:
        text = r["text"].strip()

        if not text:
            continue

        #remove exact dublication

        if text in seen_texts:
            continue

        chunk_len = len(text)

        if len(selected) >= max_chunks:
            break

        if total_chars + chunk_len > max_total_chars:
            continue    

        selected.append(r)
        total_chars += chunk_len
        seen_texts.add(text)

    return selected





