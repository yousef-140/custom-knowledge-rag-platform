from app.core.guardrails import build_guardrail_prefix


def build_prompt(query, chunks):
    context_parts = []

    for i, c in enumerate(chunks, start=1):
        context_text = c.get("compressed_text", c["text"])

        context_parts.append(
            f"""Context {i}:
[Source: {c['source']} | Page: {c['page_start']}]
{context_text}"""
        )

    context = "\n\n".join(context_parts)
    safety_prefix = build_guardrail_prefix()

    prompt = f"""
You are a retrieval-augmented question answering assistant.

{safety_prefix}

Task:
Answer the user's question using only the provided context.

Strict Rules:
1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not guess or infer unsupported facts.
4. If the answer is not explicitly supported by the context, say exactly:
Answer:
I don't know.

Sources:
- None
5. Every factual answer must include sources.
6. Only cite sources that are actually used in the answer.
7. Follow the output format exactly.

Output Format:
Answer:
<clear answer based only on context>

Sources:
- <source>, Page X
- <source>, Page Y

Context:
{context}

Question:
{query}
"""
    return prompt.strip()