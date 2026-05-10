def validate_chunks(chunks: list[dict]) -> bool:
    """
    Step 4: Input validation.
    Guards against insufficient context before LLM call.
    NEVER call generate_answer() if this returns False.

    Args:
        chunks : top-ranked chunk list from reranker

    Returns:
        True if enough context exists, False otherwise
    """
    print(f"[guardrails] Validating {len(chunks)} chunks...")
    result = len(chunks) >= 2
    print(f"[guardrails] Validation result: {result}")
    return result