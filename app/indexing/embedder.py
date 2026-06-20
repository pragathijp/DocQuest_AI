from sentence_transformers import SentenceTransformer

# Loaded once at application startup
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_embeddings(
    chunks: list[str]
) -> list[list[float]]:
    """
    Generate normalized embeddings for text chunks.

    Args:
        chunks: List of text chunks

    Returns:
        List of embedding vectors
    """

    if not chunks:
        return []

    return model.encode(
        chunks,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).tolist()