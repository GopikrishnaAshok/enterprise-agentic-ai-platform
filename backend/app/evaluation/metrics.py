
"""Deterministic evaluation metrics for RAG retrieval."""

from typing import Sequence


def precision_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Measure the proportion of relevant results in the top K."""

    if k <= 0:
        raise ValueError("k must be greater than zero")

    top_k = retrieved_ids[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(
        1 for doc_id in top_k
        if doc_id in relevant_ids
    )

    return relevant_count / len(top_k)


def recall_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Measure how many relevant documents appear in the top K."""

    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not relevant_ids:
        return 0.0

    retrieved_relevant = set(retrieved_ids[:k]) & relevant_ids

    return len(retrieved_relevant) / len(relevant_ids)


def reciprocal_rank(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str],
) -> float:
    """Return reciprocal rank of the first relevant document."""

    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank

    return 0.0
