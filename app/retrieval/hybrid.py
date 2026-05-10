def retrieve_chunks(query: str, doc_id: str) -> list[dict]:
    """
    Step 2: Chunk retrieval.
    PHASE 1 — Dummy version for pipeline testing.
    PHASE 2 — Will swap to real Qdrant + BM25 retrieval.

    Args:
        query  : rewritten user question
        doc_id : UUID from Member 1's process_document()

    Returns:
        List of dicts with 'chunk' and 'score' keys
    """
    print(f"[hybrid] Retrieving chunks for doc_id: {doc_id}")
    print(f"[hybrid] Query: {query}")

    # PHASE 1 — Dummy chunks (swap this out in Phase 2)
    return [
        {"chunk": "Operating system is a software that manages hardware and software resources.", "score": 0.9},
        {"chunk": "Process scheduling manages CPU allocation among multiple processes.", "score": 0.85},
        {"chunk": "Memory management allocates and deallocates RAM for running processes.", "score": 0.80}
    ]