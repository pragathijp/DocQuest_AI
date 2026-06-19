from rank_bm25 import BM25Okapi

from storage import load_chunks

_bm25_store: dict[str, BM25Okapi] = {}
_chunk_store: dict[str, list[str]] = {}


def build_bm25_index(doc_id: str, chunks: list[str]) -> BM25Okapi:
    tokenized = [chunk.lower().split() for chunk in chunks]

    bm25 = BM25Okapi(tokenized)

    _bm25_store[doc_id] = bm25
    _chunk_store[doc_id] = chunks

    print(
        f"[bm25_index] BM25 index built for doc_id: {doc_id} "
        f"— {len(chunks)} chunks indexed."
    )

    return bm25


def get_bm25_index(doc_id: str) -> BM25Okapi:
    if doc_id not in _bm25_store:
        print(
            f"[bm25_index] Cache miss for {doc_id}. "
            f"Rebuilding from persisted chunks..."
        )

        chunks = load_chunks(doc_id)
        build_bm25_index(doc_id, chunks)

    return _bm25_store[doc_id]


def get_chunks(doc_id: str) -> list[str]:
    if doc_id not in _chunk_store:
        chunks = load_chunks(doc_id)

        _chunk_store[doc_id] = chunks

    return _chunk_store[doc_id]