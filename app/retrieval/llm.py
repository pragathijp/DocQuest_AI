import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Create client only if API key exists
client = None
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)


def generate_answer(
    query: str,
    context: list[dict],
    history: list[dict] | None = None
) -> dict:
    """
    Step 5: LLM answer generation.
    Calls Gemini 2.5 Flash with query + context + chat history.
    """

    # Avoid mutable default argument
    history = history or []

    # Prevent crashes during CI/testing when no API key is available
    if client is None:
        raise RuntimeError("GEMINI_API_KEY not configured")

    print(f"[llm] Generating answer for query: {query}")

    context_text = "\n\n".join([c["chunk"] for c in context])

    # Return only short previews instead of full chunks
    source_chunks = [
        {
            "preview": (
                c["chunk"][:150] + "..."
                if len(c["chunk"]) > 150
                else c["chunk"]
            )
        }
        for c in context
    ]

    # Keep confidence between 0 and 1
    confidence = (
        round(min(1.0, context[0]["score"]), 3)
        if context else 0.0
    )

    # Build conversation history string
    history_text = ""
    if history:
        history_text = "PREVIOUS CONVERSATION:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
        history_text += "\n"

    prompt = f"""Answer ONLY using the context below. You may refer to the previous conversation if relevant.
Do not use outside knowledge. If the answer is not in the context, say 'Not found in document.'

{history_text}CONTEXT:
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
        "answer": answer,
        "sources": source_chunks,
        "confidence": confidence
    }