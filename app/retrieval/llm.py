from google import genai

client = genai.Client(api_key="AIzaSyCd9pTGY0rEi6qtj1bZlHA70he8HW792Ms")

def generate_answer(query: str, context: list[dict]) -> dict:
    """
    Step 5: LLM answer generation.
    Calls Gemini 2.5 Flash with query + context.
    NEVER uses outside knowledge — only context provided.

    Args:
        query   : rewritten user question
        context : validated top chunks from reranker

    Returns:
        {"answer": str, "sources": list[str], "confidence": float}
    """
    print(f"[llm] Generating answer for query: {query}")

    context_text  = "\n\n".join([c["chunk"] for c in context])
    source_chunks = [c["chunk"] for c in context]
    confidence    = context[0]["score"] if context else 0.0

    prompt = f"""Answer ONLY using the context below. Do not use outside knowledge.
If the answer is not in the context, say 'Not found in document.'

CONTEXT:
{context_text}

QUESTION: {query}

ANSWER:"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    answer = response.text.strip()

    print(f"[llm] Answer generated. Confidence: {confidence}")

    return {
        "answer":     answer,
        "sources":    source_chunks,
        "confidence": confidence
    }