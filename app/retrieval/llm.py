from google import genai

from app.config import GOOGLE_API_KEY
from app.utils.logger import get_logger

logger = get_logger(__name__)

# ==========================================
# Gemini Client
# ==========================================

client = genai.Client(
    api_key=GOOGLE_API_KEY
)

logger.info(
    "Gemini client initialized"
)


def generate_answer(
    query: str,
    context: list[dict],
    history: list[dict] | None = None,
) -> dict:
    """
    Generate answer using Gemini 2.5 Flash.
    """

    history = history or []

    logger.info(
        f"Generating answer for query: {query}"
    )

    context_text = "\n\n".join(
        c["chunk"]
        for c in context
    )

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

    # ==========================================
    # Confidence Estimation
    # ==========================================

    if context:
        rerank_score = context[0].get(
            "rerank_score",
            -100,
        )

        if rerank_score >= -3:
            confidence = "High"
        elif rerank_score >= -8:
            confidence = "Medium"
        else:
            confidence = "Low"
    else:
        confidence = "Low"

    # ==========================================
    # Conversation History
    # ==========================================

    history_text = ""

    if history:
        history_text = (
            "PREVIOUS CONVERSATION:\n"
        )

        for msg in history:
            role = (
                "User"
                if msg["role"] == "user"
                else "Assistant"
            )

            history_text += (
                f"{role}: "
                f"{msg['content']}\n"
            )

        history_text += "\n"

    prompt = f"""
Answer ONLY using the context below.

You may refer to the previous conversation if relevant.

Do not use outside knowledge.

If the answer is not in the context,
say exactly:

Not found in document.

{history_text}

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
"""

    try:
        response = (
            client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
        )

        answer = response.text.strip()

    except Exception as e:
        logger.exception(
            "Gemini generation failed"
        )

        answer = (
            "Unable to generate answer "
            "at this time."
        )

    logger.info(
        f"Answer generated "
        f"(confidence={confidence})"
    )

    return {
        "answer": answer,
        "sources": source_chunks,
        "confidence": confidence,
    }