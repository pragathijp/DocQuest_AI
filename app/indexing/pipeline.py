import uuid
import sys
import os

# Make sure imports work when run from any directory
sys.path.insert(0, os.path.dirname(__file__))

from extractor import extract_text
from cleaner import clean_text
from chunker import chunk_text
from embedder import generate_embeddings
from qdrant_store import store_vectors
from bm25_index import build_bm25_index
from storage import save_chunks
from app.utils.logger import get_logger

logger = get_logger(__name__)


def process_document(file_path: str) -> dict:
    """
    Full 6-step pipeline: PDF → indexed knowledge base.

    Args:
        file_path : Absolute or relative path to a PDF file

    Returns:
        {"doc_id": "<uuid>", "status": "indexed"}

    Raises:
        ValueError if any step fails (empty PDF, bad file, etc.)
    """

    logger.info(f"Starting pipeline for: {file_path}")

    # Step 1 — Extract
    logger.info("Step 1/6 - Extracting text")
    text = extract_text(file_path)

    if not text.strip():
        raise ValueError("Pipeline aborted: PDF has no extractable text.")

    logger.info(f"Extracted {len(text)} characters")

    # Step 2 — Clean
    logger.info("Step 2/6 - Cleaning text")
    cleaned = clean_text(text)

    logger.info(f"Cleaned text: {len(cleaned)} characters")

    # Step 3 — Chunk
    logger.info("Step 3/6 - Chunking text")
    chunks = chunk_text(cleaned)

    if not chunks:
        raise ValueError("Pipeline aborted: No chunks produced after splitting.")

    logger.info(f"Produced {len(chunks)} chunks")

    # Step 4 — Embed
    logger.info("Step 4/6 - Generating embeddings")
    vectors = generate_embeddings(chunks)

    if len(vectors) != len(chunks):
        raise ValueError(
            f"Pipeline aborted: {len(chunks)} chunks but {len(vectors)} vectors."
        )

    logger.info(
        f"Generated {len(vectors)} vectors (dim={len(vectors[0])})"
    )

    # Step 5 — Store in Qdrant
    doc_id = str(uuid.uuid4())

    logger.info(
        f"Step 5/6 - Storing vectors in Qdrant (doc_id={doc_id})"
    )

    store_vectors(doc_id, chunks, vectors)

    # Step 6 — Save chunks + Build BM25
    logger.info(
        "Step 6/6 - Saving chunks and building BM25 index"
    )

    save_chunks(doc_id, chunks)
    build_bm25_index(doc_id, chunks)

    logger.info(
        f"Pipeline complete. doc_id={doc_id}"
    )

    return {
        "doc_id": doc_id,
        "status": "indexed"
    }