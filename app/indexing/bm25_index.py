from rank_bm25 import BM25Okapi

# In-memory store: maps doc_id → BM25 index
# Member 2 (Retrieval) will call get_bm25_index(doc_id) to fetch this
_bm25_store: dict[str, BM25Okapi] = {}


def build_bm25_index(doc_id: str, chunks: list[str]) -> BM25Okapi:
    """
    Tokenize chunks and build a BM25 keyword index for a document.

    Args:
        doc_id : Unique document identifier (UUID string)
        chunks : List of text chunk strings

    Returns:
        BM25Okapi index object (also stored in memory by doc_id)
    """
    if not chunks:
        raise ValueError(f"Cannot build BM25 index: chunk list is empty for doc_id={doc_id}")

    tokenized = [chunk.lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized)

    _bm25_store[doc_id] = bm25
    print(f"[bm25_index] BM25 index built for doc_id: {doc_id} — {len(chunks)} chunks indexed.")
    return bm25


def get_bm25_index(doc_id: str) -> BM25Okapi:
    """
    Retrieve a previously built BM25 index by doc_id.
    Called by Member 2 (Retrieval) during query time.

    Raises:
        KeyError if doc_id was never indexed
    """
    if doc_id not in _bm25_store:
        raise KeyError(f"No BM25 index found for doc_id: {doc_id}. Was it indexed?")
    return _bm25_store[doc_id]