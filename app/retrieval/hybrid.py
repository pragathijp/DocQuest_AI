import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'indexing'))

from qdrant_client import QdrantClient
from embedder import generate_embeddings
from bm25_index import get_bm25_index, get_chunks

client = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "docs"

SEMANTIC_TOP_K = 20
BM25_TOP_K = 20
RRF_K = 60
FINAL_TOP_K = 10


def rrf_fusion(
    semantic_chunks: list[dict],
    bm25_chunks: list[dict],
    k: int = RRF_K
) -> list[dict]:
    """
    Reciprocal Rank Fusion (RRF)

    Combines:
    - Dense Retrieval (Qdrant)
    - Sparse Retrieval (BM25)

    Formula:
        score += 1 / (k + rank)
    """

    rrf_scores = {}

    # Dense ranking
    for rank, item in enumerate(
        sorted(semantic_chunks, key=lambda x: x["score"], reverse=True)
    ):
        chunk = item["chunk"]

        rrf_scores[chunk] = (
            rrf_scores.get(chunk, 0)
            + 1 / (k + rank + 1)
        )

    # BM25 ranking
    for rank, item in enumerate(
        sorted(bm25_chunks, key=lambda x: x["score"], reverse=True)
    ):
        chunk = item["chunk"]

        rrf_scores[chunk] = (
            rrf_scores.get(chunk, 0)
            + 1 / (k + rank + 1)
        )

    fused = [
        {
            "chunk": chunk,
            "score": score
        }
        for chunk, score in rrf_scores.items()
    ]

    fused.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return fused[:FINAL_TOP_K]


def retrieve_chunks(query: str, doc_id: str) -> list[dict]:
    """
    Hybrid Retrieval Pipeline

    Query
      ↓
    Dense Search (Top 20)
      +
    BM25 Search (Top 20)
      ↓
    RRF Fusion
      ↓
    Top 10 Chunks
    """

    print(f"[hybrid] Retrieving chunks for doc_id: {doc_id}")
    print(f"[hybrid] Query: {query}")

    # =========================
    # Dense Retrieval (Qdrant)
    # =========================

    query_vector = generate_embeddings([query])[0]

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter={
            "must": [
                {
                    "key": "doc_id",
                    "match": {"value": doc_id}
                }
            ]
        },
        limit=SEMANTIC_TOP_K
    ).points

    semantic_chunks = [
        {
            "chunk": h.payload["chunk_text"],
            "score": float(h.score)
        }
        for h in hits
    ]

    print(f"[hybrid] Semantic retrieved: {len(semantic_chunks)}")

    # =========================
    # BM25 Retrieval
    # =========================

    bm25_chunks = []

    try:
        bm25 = get_bm25_index(doc_id)
        chunks_list = get_chunks(doc_id)

        tokenized_query = query.lower().split()

        scores = bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:BM25_TOP_K]

        bm25_chunks = [
            {
                "chunk": chunks_list[idx],
                "score": float(scores[idx])
            }
            for idx in top_indices
        ]

    except KeyError as e:
        print(f"[hybrid] BM25 unavailable: {e}")

    print(f"[hybrid] BM25 retrieved: {len(bm25_chunks)}")

    # =========================
    # RRF Fusion
    # =========================

    fused_chunks = rrf_fusion(
        semantic_chunks,
        bm25_chunks
    )

    print(f"[retrieval] Query: {query}")
    print(f"[retrieval] Dense retrieved: {len(semantic_chunks)}")
    print(f"[retrieval] BM25 retrieved: {len(bm25_chunks)}")
    print(f"[retrieval] After RRF: {len(fused_chunks)}")

    return fused_chunks