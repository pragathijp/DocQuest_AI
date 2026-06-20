from app.retrieval.rewrite import rewrite_query
from app.retrieval.hybrid import retrieve_chunks
from app.retrieval.reranker import rerank_chunks
from app.retrieval.guardrails import validate_chunks
from app.retrieval.llm import generate_answer

from app.utils.logger import get_logger

logger = get_logger(__name__)


def process_query(
    query: str,
    doc_id: str,
    history: list[dict] | None = None,
) -> dict:
    """
    Production Retrieval Pipeline

    Query
      ↓
    Query Rewriting
      ↓
    Hybrid Retrieval (Dense + BM25 + RRF)
      ↓
    CrossEncoder Reranking
      ↓
    Guardrails Validation
      ↓
    Gemini Answer Generation
      ↓
    Final Response
    """

    history = history or []

    logger.info("Starting retrieval pipeline")
    logger.info(f"Query: {query}")
    logger.info(f"doc_id: {doc_id}")

    # ==========================================
    # Step 1 - Query Rewriting
    # ==========================================

    logger.info("Step 1/5 - Rewriting query")

    rewritten_query = rewrite_query(query)

    logger.info(
        f"Rewritten query: {rewritten_query}"
    )

    # ==========================================
    # Step 2 - Hybrid Retrieval
    # ==========================================

    logger.info(
        "Step 2/5 - Retrieving chunks"
    )

    chunks = retrieve_chunks(
        rewritten_query,
        doc_id,
    )

    if not chunks:
        logger.warning(
            "No chunks retrieved"
        )

        return {
            "answer": (
                "No relevant information "
                "found in the document."
            ),
            "sources": [],
            "confidence": 0.0,
        }

    logger.info(
        f"Retrieved {len(chunks)} chunks"
    )

    # ==========================================
    # Step 3 - CrossEncoder Reranking
    # ==========================================

    logger.info(
        "Step 3/5 - Reranking chunks"
    )

    top_chunks = rerank_chunks(
        chunks,
        rewritten_query,
    )

    if not top_chunks:
        logger.warning(
            "Reranker returned no chunks"
        )

        return {
            "answer": (
                "No relevant information "
                "found in the document."
            ),
            "sources": [],
            "confidence": 0.0,
        }

    logger.info(
        f"Top chunks after reranking: "
        f"{len(top_chunks)}"
    )

    # ==========================================
    # Step 4 - Guardrails Validation
    # ==========================================

    logger.info(
        "Step 4/5 - Validating chunks"
    )

    if not validate_chunks(
        top_chunks
    ):
        logger.warning(
            "Guardrail validation failed"
        )

        return {
            "answer": (
                "No relevant information "
                "found in the document."
            ),
            "sources": [],
            "confidence": 0.0,
        }

    # ==========================================
    # Step 5 - Answer Generation
    # ==========================================

    logger.info(
        "Step 5/5 - Generating answer"
    )

    result = generate_answer(
        rewritten_query,
        top_chunks,
        history,
    )

    logger.info(
        "Retrieval pipeline completed successfully"
    )

    return result