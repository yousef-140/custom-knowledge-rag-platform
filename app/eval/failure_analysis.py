def analyze_single_case(query, target_chunk_id, results, top_n=5):
    print("=" * 80)
    print("QUERY:")
    print(query)
    print("-" * 80)

    found_rank = None

    for rank, r in enumerate(results[:top_n], start=1):
        print(f"Rank {rank} | chunk_id={r.get('chunk_id')} | score={r.get('score', r.get('hybrid_score', 'N/A'))}")
        print(r["text"][:200].replace("\n", " "))
        print("-" * 40)

        if r.get("chunk_id") == target_chunk_id:
            found_rank = rank

    if found_rank is None:
        print("FAILURE TYPE: Retrieval Failure (target chunk not found in top results)")
    else:
        print(f"Target chunk found at rank {found_rank}")
        if found_rank == 1:
            print("Retrieval looks good. If final answer is wrong, likely Prompt/Generation Failure.")
        else:
            print("Possible Ranking Failure: correct chunk found but not at top rank.")

    print("=" * 80)