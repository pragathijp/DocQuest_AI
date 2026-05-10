def rewrite_query(query: str, history: list = []) -> str:
    """
    Step 1: Query rewriting.
    Start simple — returns query as-is.
    Later: expand with LLM-based rewriting.

    Args:
        query   : raw user question
        history : optional conversation history (unused for now)

    Returns:
        Rewritten query string
    """
    print(f"[rewrite] Query received: {query}")
    return query