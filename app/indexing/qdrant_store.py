from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "docs"
VECTOR_DIM = 384


def ensure_collection_exists():
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_DIM,
                distance=Distance.COSINE,
            ),
        )
        print(f"[qdrant_store] Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"[qdrant_store] Collection '{COLLECTION_NAME}' already exists.")


def store_vectors(doc_id: str, chunks: list[str], vectors: list):
    if len(chunks) != len(vectors):
        raise ValueError(
            f"Mismatch: {len(chunks)} chunks but {len(vectors)} vectors. "
            "They must be equal."
        )

    ensure_collection_exists()

    points = [
        PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                "doc_id": doc_id,
                "chunk_text": chunk,
                "chunk_index": i,
            },
        )
        for i, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(
        f"[qdrant_store] Stored {len(points)} vectors "
        f"for doc_id: {doc_id}"
    )