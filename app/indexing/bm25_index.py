from rank_bm25 import BM25Okapi

_bm25_store: dict[str, BM25Okapi] = {}
_chunk_store: dict[str, list[str]] = {}  # stores original chunks


def build_bm25_index(doc_id: str, chunks: list[str]) -> BM25Okapi:
    tokenized = [chunk.lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized)
    _bm25_store[doc_id] = bm25
    _chunk_store[doc_id] = chunks  # save original chunks
    print(f"[bm25_index] BM25 index built for doc_id: {doc_id} — {len(chunks)} chunks indexed.")
    return bm25


def get_bm25_index(doc_id: str) -> BM25Okapi:
    if doc_id not in _bm25_store:
        raise KeyError(f"No BM25 index found for doc_id: {doc_id}. Was it indexed?")
    return _bm25_store[doc_id]


def get_chunks(doc_id: str) -> list[str]:
    if doc_id not in _chunk_store:
        raise KeyError(f"No chunks found for doc_id: {doc_id}. Was it indexed?")
    return _chunk_store[doc_id]