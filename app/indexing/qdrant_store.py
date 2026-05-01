from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Connect to Qdrant running locally via Docker
client = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "docs"
VECTOR_DIM = 384  # all-MiniLM-L6-v2 output dimension


def ensure_collection_exists():
    """Create the 'docs' collection if it doesn't already exist."""
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )
        print(f"[qdrant_store] Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"[qdrant_store] Collection '{COLLECTION_NAME}' already exists.")


def store_vectors(doc_id: str, chunks: list[str], vectors: list):
    """
    Store chunk vectors and metadata into Qdrant.

    Args:
        doc_id  : Unique document identifier (UUID string)
        chunks  : List of text chunk strings
        vectors : List of embedding vectors (one per chunk)
    """
    if len(chunks) != len(vectors):
        raise ValueError(
            f"Mismatch: {len(chunks)} chunks but {len(vectors)} vectors. "
            "They must be equal."
        )

    ensure_collection_exists()

    points = [
        PointStruct(
            id=i,
            vector=vector,
            payload={
                "doc_id": doc_id,
                "chunk_text": chunk,
                "chunk_index": i,
            },
        )
        for i, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"[qdrant_store] Stored {len(points)} vectors for doc_id: {doc_id}")