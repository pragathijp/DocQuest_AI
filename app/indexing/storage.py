import os
import pickle
from pathlib import Path

from app.utils.logger import get_logger

logger = get_logger(__name__)

STORAGE_DIR = Path("storage/bm25")
STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_chunks(
    doc_id: str,
    chunks: list[str]
) -> None:
    filepath = STORAGE_DIR / f"{doc_id}.pkl"

    with open(filepath, "wb") as f:
        pickle.dump(chunks, f)

    logger.info(
        f"Saved {len(chunks)} chunks "
        f"for doc_id={doc_id}"
    )


def load_chunks(
    doc_id: str
) -> list[str]:
    filepath = STORAGE_DIR / f"{doc_id}.pkl"

    if not filepath.exists():
        raise FileNotFoundError(
            f"No stored chunks found for "
            f"doc_id={doc_id}"
        )

    with open(filepath, "rb") as f:
        chunks = pickle.load(f)

    logger.info(
        f"Loaded {len(chunks)} chunks "
        f"for doc_id={doc_id}"
    )

    return chunks