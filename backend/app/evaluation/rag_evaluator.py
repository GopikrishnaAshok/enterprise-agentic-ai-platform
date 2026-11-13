
"""Evaluate RAG retrieval results using deterministic metrics."""

from backend.app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def evaluate_retrieval(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int = 5,
) -> dict:
    """Return retrieval quality metrics."""

    if k <= 0:
        raise ValueError("k must be greater than zero")

    return {
        "precision_at_k": precision_at_k(
            retrieved_ids, relevant_ids, k
        ),
        "recall_at_k": recall_at_k(
            retrieved_ids, relevant_ids, k
        ),
        "reciprocal_rank": reciprocal_rank(
            retrieved_ids, relevant_ids
        ),
        "retrieved_count": len(retrieved_ids[:k]),
        "relevant_count": len(relevant_ids),
    }
