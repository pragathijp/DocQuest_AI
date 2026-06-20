from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


def generate_embeddings(
    chunks: list[str]
) -> list[list[float]]:
    if not chunks:
        return []

    model = get_model()

    return model.encode(
        chunks,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).tolist()