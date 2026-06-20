_model = None


def get_model():
    global _model

    print("EMBEDDER STEP 1")

    if _model is None:

        print("EMBEDDER STEP 2")

        from sentence_transformers import (
            SentenceTransformer,
        )

        print("EMBEDDER STEP 3")

        print("LOADING MODEL NOW")

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("MODEL LOADED")

        print("EMBEDDER STEP 4")

    return _model


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

    print("EMBEDDER STEP 5")

    if not chunks:
        return []

    model = get_model()

    print("EMBEDDER STEP 6")

    embeddings = model.encode(
        chunks,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    print("EMBEDDER STEP 7")

    return embeddings.tolist()