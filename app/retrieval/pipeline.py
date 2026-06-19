import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from rewrite import rewrite_query
from hybrid import retrieve_chunks
from reranker import rerank_chunks
from guardrails import validate_chunks
from llm import generate_answer


def process_query(
    query: str,
    doc_id: str,
    history: list[dict] | None = None
) -> dict:
    """
    Main orchestrator — connects all 5 modules in order.

    Args:
        query   : raw user question
        doc_id  : UUID from Member 1's process_document()
        history : list of previous messages
                 [{"role": "user"/"assistant", "content": "..."}]

    Returns:
        {"answer": str, "sources": list, "confidence": float}
    """

    # Avoid mutable default argument bug
    history = history or []

    print(f"\n[pipeline] ── Starting retrieval pipeline")
    print(f"[pipeline] Query: {query}")
    print(f"[pipeline] doc_id: {doc_id}")

    # Step 1 — Rewrite query
    print("[pipeline] Step 1/5 — Rewriting query...")
    q = rewrite_query(query)

    # Step 2 — Retrieve chunks
    print("[pipeline] Step 2/5 — Retrieving chunks...")
    chunks = retrieve_chunks(q, doc_id)

    # Step 3 — Rerank
    print("[pipeline] Step 3/5 — Reranking chunks...")
    top_chunks = rerank_chunks(chunks, q)

    # Step 4 — Validate
    print("[pipeline] Step 4/5 — Validating chunks...")
    if not validate_chunks(top_chunks):
        print("[pipeline] Guard triggered — returning fallback.")
        return {
            "answer": "No relevant info found",
            "sources": [],
            "confidence": 0.0
        }

    # Step 5 — Generate answer
    print("[pipeline] Step 5/5 — Generating answer...")
    result = generate_answer(q, top_chunks, history)

    print("[pipeline] ── Pipeline complete.\n")

    return result