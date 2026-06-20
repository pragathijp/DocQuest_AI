from uuid import uuid4

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
)

from app.qdrant_client import client
from app.utils.logger import get_logger

logger = get_logger(__name__)

COLLECTION_NAME = "docs"
VECTOR_DIM = 384


def ensure_collection_exists() -> None:
    existing = [
        c.name
        for c in client.get_collections().collections
    ]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_DIM,
                distance=Distance.COSINE,
            ),
        )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="doc_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        logger.info(
            f"Collection '{COLLECTION_NAME}' created "
            f"with payload index on doc_id."
        )

    else:
        try:
            client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name="doc_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
        except Exception:
            pass

        logger.info(
            f"Collection '{COLLECTION_NAME}' already exists."
        )


def store_vectors(
    doc_id: str,
    chunks: list[str],
    vectors: list[list[float]],
) -> None:
    if len(chunks) != len(vectors):
        raise ValueError(
            f"Mismatch: {len(chunks)} chunks "
            f"but {len(vectors)} vectors."
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
        for i, (chunk, vector)
        in enumerate(zip(chunks, vectors))
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True,
    )

    logger.info(
        f"Stored {len(points)} vectors "
        f"for doc_id={doc_id}"
    )