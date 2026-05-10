import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'indexing'))

from qdrant_client import QdrantClient
from embedder import generate_embeddings
from bm25_index import get_bm25_index, get_chunks

client = QdrantClient("localhost", port=6333)
COLLECTION_NAME = "docs"

def retrieve_chunks(query: str, doc_id: str) -> list[dict]:
    """
    Step 2: Hybrid retrieval — Qdrant (semantic) + BM25 (keyword).

    Args:
        query  : rewritten user question
        doc_id : UUID from Member 1's process_document()

    Returns:
        List of dicts with 'chunk' and 'score' keys
    """
    print(f"[hybrid] Retrieving chunks for doc_id: {doc_id}")
    print(f"[hybrid] Query: {query}")

    # --- Semantic search via Qdrant ---
    query_vector = generate_embeddings([query])[0]
    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter={
            "must": [{"key": "doc_id", "match": {"value": doc_id}}]
        },
        limit=5
    ).points

    semantic_chunks = [
        {"chunk": h.payload["chunk_text"], "score": h.score}
        for h in hits
    ]
    print(f"[hybrid] Semantic hits: {len(semantic_chunks)}")

    # --- Keyword search via BM25 ---
    bm25 = get_bm25_index(doc_id)
    chunks_list = get_chunks(doc_id)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]

    bm25_chunks = [
        {"chunk": chunks_list[top_indices[i]], "score": float(scores[top_indices[i]])}
        for i in range(len(top_indices))
        if scores[top_indices[i]] > 0
    ]
    print(f"[hybrid] BM25 hits: {len(bm25_chunks)}")

    # --- Fuse both ---
    combined = semantic_chunks + bm25_chunks
    print(f"[hybrid] Total combined chunks: {len(combined)}")
    return combined