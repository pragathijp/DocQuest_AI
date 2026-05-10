def rerank_chunks(chunks: list[dict]) -> list[dict]:
    """
    Step 3: Reranking.
    Sorts chunks by score descending, keeps top 3.

    Args:
        chunks : list of dicts with 'chunk' and 'score' keys

    Returns:
        Top 3 chunks sorted by score descending
    """
    print(f"[reranker] Reranking {len(chunks)} chunks...")
    reranked = sorted(chunks, key=lambda x: x["score"], reverse=True)[:3]
    print(f"[reranker] Top {len(reranked)} chunks selected.")
    return reranked