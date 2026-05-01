from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks: list) -> list:
    return model.encode(chunks, batch_size=32).tolist()