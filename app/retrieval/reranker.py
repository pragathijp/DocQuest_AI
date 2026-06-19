from sentence_transformers import CrossEncoder

# Load once at startup
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

print("=== CROSSENCODER RERANKER LOADED ===")


def rerank_chunks(chunks: list[dict], query: str) -> list[dict]:
    """
    CrossEncoder reranking.

    Args:
        chunks : retrieved chunks
        query  : user query

    Returns:
        Top 3 reranked chunks
    """

    if not chunks:
        return []

    print(f"[reranker] CrossEncoder reranking {len(chunks)} chunks...")

    pairs = [
        (query, chunk["chunk"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)
        print(f"[reranker] Score: {float(score):.4f}")

    reranked = sorted(
        chunks,
        key=lambda x: x["rerank_score"],
        reverse=True
    )[:3]

    print(f"[reranker] Top {len(reranked)} chunks selected.")

    return reranked