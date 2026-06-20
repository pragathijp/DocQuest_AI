from sentence_transformers import CrossEncoder

from app.utils.logger import get_logger

logger = get_logger(__name__)

# ==========================================
# Load model once at startup
# ==========================================

_model = None



def get_model():
    global _model

    if _model is None:
        logger.info(
            "Loading CrossEncoder model..."
        )

        _model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return _model



def rerank_chunks(
    chunks: list[dict],
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    CrossEncoder reranking.

    Args:
        chunks : Retrieved chunks
        query  : User query
        top_k  : Number of chunks to keep

    Returns:
        Top reranked chunks
    """

    if not chunks:
        return []

    logger.info(
        f"Reranking {len(chunks)} chunks"
    )

    valid_chunks = [
        chunk
        for chunk in chunks
        if "chunk" in chunk
    ]

    if not valid_chunks:
        logger.warning(
            "No valid chunks found for reranking"
        )
        return []

    pairs = [
        (
            query,
            chunk["chunk"]
        )
        for chunk in valid_chunks
    ]

    model = get_model()

    scores = model.predict(pairs)

    for chunk, score in zip(
        valid_chunks,
        scores
    ):
        chunk["rerank_score"] = float(
            score
        )

    reranked = sorted(
        valid_chunks,
        key=lambda x: x["rerank_score"],
        reverse=True,
    )[:top_k]

    logger.info(
        f"Selected top {len(reranked)} chunks"
    )

    return reranked