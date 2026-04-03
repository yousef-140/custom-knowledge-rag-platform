def recall_at_k(retriever, questions, k=5):

    correct = 0

    for item in questions:

        q = item["question"]
        target = item["chunk_id"]

        results = retriever.search(q, top_k=k)

        retrieved_ids = [r["chunk_id"] for r in results]

        if target in retrieved_ids:
            correct += 1

    return correct / len(questions)