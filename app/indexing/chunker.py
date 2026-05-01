def chunk_text(text: str, size: int = 300, overlap: int = 50) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = words[i : i + size]
        chunks.append(" ".join(chunk))
    return chunks