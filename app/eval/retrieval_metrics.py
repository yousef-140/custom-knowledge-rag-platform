def recall_at_k(retriever, questions, k=5):
    if not questions:
        return 0.0
    
    correct = 0
    for item in questions:
        query= item["question"]
        target_chunk_id = item["chunk_id"]

        results = retriever.search(query, top_k=k)

        retrieved_ids = [r["chunk_id"] for r in results]

        if target_chunk_id in retrieved_ids:
            correct += 1

    return correct / len(questions)


def mrr_at_k(retriever, questions, k=5):
    if not questions:
        return 0.0
    
    total_score = 0 

    for item in questions:
        query= item["question"]
        target_chunk_id = item["chunk_id"]

        results = retriever.search(query, top_k=k)

        retrieved_ids = [r["chunk_id"] for r in results]

        recipocal_rank = 0.0

        for rank,chunk_id in enumerate(retrieved_ids, start=1):
            if chunk_id == target_chunk_id:
                recipocal_rank = 1 / rank
                break

        total_score += recipocal_rank


    return total_score / len(questions)





    
    