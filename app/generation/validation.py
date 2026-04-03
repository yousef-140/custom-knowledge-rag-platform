def validate_answer_format(answer: str) -> dict:
    if not answer:
        return {
            "valid": False,
            "reason": "empty answer"
        }

    has_answer = "Answer:" in answer
    has_sources = "Sources:" in answer

    if not has_answer or not has_sources:
        return {
            "valid": False,
            "reason": "missing Answer or Sources section"
        }

    return {
        "valid": True,
        "reason": "ok"
    }