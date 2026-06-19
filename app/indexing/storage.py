import os
import pickle

STORAGE_DIR = "storage/bm25"

os.makedirs(STORAGE_DIR, exist_ok=True)


def save_chunks(doc_id: str, chunks: list[str]) -> None:
    filepath = os.path.join(STORAGE_DIR, f"{doc_id}.pkl")

    with open(filepath, "wb") as f:
        pickle.dump(chunks, f)


def load_chunks(doc_id: str) -> list[str]:
    filepath = os.path.join(STORAGE_DIR, f"{doc_id}.pkl")

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"No stored chunks found for doc_id: {doc_id}"
        )

    with open(filepath, "rb") as f:
        return pickle.load(f)