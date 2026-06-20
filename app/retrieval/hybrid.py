from app.indexing.embedder import (
    generate_embeddings,
)
from app.indexing.bm25_index import (
    get_bm25_index,
    get_chunks,
)
from app.qdrant_client import client
from app.utils.logger import get_logger

logger = get_logger(__name__)

COLLECTION_NAME = "docs"

SEMANTIC_TOP_K = 20
BM25_TOP_K = 20
RRF_K = 60
FINAL_TOP_K = 10


def rrf_fusion(
    semantic_chunks: list[dict],
    bm25_chunks: list[dict],
    k: int = RRF_K,
) -> list[dict]:
    """
    Reciprocal Rank Fusion (RRF)

    Combines:
    - Dense Retrieval
    - BM25 Retrieval

    Formula:
        score += 1 / (k + rank)
    """

    rrf_scores = {}

    # Dense ranking
    for rank, item in enumerate(
        sorted(
            semantic_chunks,
            key=lambda x: x["score"],
            reverse=True,
        )
    ):
        chunk = item["chunk"]

        rrf_scores[chunk] = (
            rrf_scores.get(chunk, 0)
            + 1 / (k + rank + 1)
        )

    # BM25 ranking
    for rank, item in enumerate(
        sorted(
            bm25_chunks,
            key=lambda x: x["score"],
            reverse=True,
        )
    ):
        chunk = item["chunk"]

        rrf_scores[chunk] = (
            rrf_scores.get(chunk, 0)
            + 1 / (k + rank + 1)
        )

    fused = [
        {
            "chunk": chunk,
            "score": score,
        }
        for chunk, score in rrf_scores.items()
    ]

    fused.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return fused[:FINAL_TOP_K]


def retrieve_chunks(
    query: str,
    doc_id: str,
) -> list[dict]:
    """
    Hybrid Retrieval Pipeline

    Query
      ↓
    Dense Retrieval (Qdrant)
      +
    BM25 Retrieval
      ↓
    Reciprocal Rank Fusion
      ↓
    Top Chunks
    """

    logger.info(
        f"Retrieving chunks for doc_id={doc_id}"
    )

    logger.info(
        f"Query={query}"
    )

    # ==========================================
    # Dense Retrieval
    # ==========================================

    query_embeddings = generate_embeddings(
        [query]
    )

    if not query_embeddings:
        logger.warning(
            "Failed to generate query embedding"
        )
        return []

    query_vector = query_embeddings[0]

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter={
            "must": [
                {
                    "key": "doc_id",
                    "match": {
                        "value": doc_id
                    }
                }
            ]
        },
        limit=SEMANTIC_TOP_K,
    ).points

    semantic_chunks = [
        {
            "chunk": h.payload["chunk_text"],
            "score": float(h.score),
        }
        for h in hits
    ]

    logger.info(
        f"Semantic retrieved: "
        f"{len(semantic_chunks)}"
    )

    # ==========================================
    # BM25 Retrieval
    # ==========================================

    bm25_chunks = []

    try:
        bm25 = get_bm25_index(
            doc_id
        )

        chunks_list = get_chunks(
            doc_id
        )

        tokenized_query = (
            query.lower().split()
        )

        scores = bm25.get_scores(
            tokenized_query
        )

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:BM25_TOP_K]

        bm25_chunks = [
            {
                "chunk": chunks_list[idx],
                "score": float(scores[idx]),
            }
            for idx in top_indices
        ]

    except Exception as e:
        logger.warning(
            f"BM25 unavailable: {e}"
        )

    logger.info(
        f"BM25 retrieved: "
        f"{len(bm25_chunks)}"
    )

    # ==========================================
    # RRF Fusion
    # ==========================================

    fused_chunks = rrf_fusion(
        semantic_chunks,
        bm25_chunks,
    )

    logger.info(
        f"After RRF: "
        f"{len(fused_chunks)}"
    )

    return fused_chunks