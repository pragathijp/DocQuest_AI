from rank_bm25 import BM25Okapi

from app.indexing.storage import load_chunks
from app.utils.logger import get_logger

logger = get_logger(__name__)

_bm25_store: dict[str, BM25Okapi] = {}
_chunk_store: dict[str, list[str]] = {}


def build_bm25_index(
    doc_id: str,
    chunks: list[str]
) -> BM25Okapi:
    tokenized = [
        chunk.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized)

    _bm25_store[doc_id] = bm25
    _chunk_store[doc_id] = chunks

    logger.info(
        f"BM25 index built for "
        f"doc_id={doc_id} "
        f"({len(chunks)} chunks)"
    )

    return bm25


def get_bm25_index(
    doc_id: str
) -> BM25Okapi:
    if doc_id not in _bm25_store:
        logger.info(
            f"BM25 cache miss "
            f"for doc_id={doc_id}"
        )

        chunks = load_chunks(doc_id)

        build_bm25_index(
            doc_id,
            chunks
        )

    return _bm25_store[doc_id]


def get_chunks(
    doc_id: str
) -> list[str]:
    if doc_id not in _chunk_store:
        chunks = load_chunks(doc_id)

        _chunk_store[doc_id] = chunks

    return _chunk_store[doc_id]