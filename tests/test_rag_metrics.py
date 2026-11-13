
"""Tests for the RAG evaluation engine."""

import pytest

from backend.app.evaluation.rag_evaluator import (
    evaluate_retrieval,
)


def test_evaluate_retrieval():
    result = evaluate_retrieval(
        retrieved_ids=["doc1", "doc2", "doc3"],
        relevant_ids={"doc1", "doc3"},
        k=3,
    )

    assert result["precision_at_k"] == pytest.approx(2 / 3)
    assert result["recall_at_k"] == 1.0
    assert result["reciprocal_rank"] == 1.0
    assert result["retrieved_count"] == 3
    assert result["relevant_count"] == 2


def test_no_retrieved_documents():
    result = evaluate_retrieval(
        retrieved_ids=[],
        relevant_ids={"doc1"},
        k=5,
    )

    assert result["precision_at_k"] == 0.0
    assert result["recall_at_k"] == 0.0
    assert result["reciprocal_rank"] == 0.0


def test_invalid_k():
    with pytest.raises(ValueError):
        evaluate_retrieval(
            retrieved_ids=["doc1"],
            relevant_ids={"doc1"},
            k=0,
        )


def test_partial_retrieval():
    result = evaluate_retrieval(
        retrieved_ids=["doc1", "doc2"],
        relevant_ids={"doc1", "doc3"},
        k=2,
    )

    assert result["precision_at_k"] == 0.5
    assert result["recall_at_k"] == 0.5
    assert result["reciprocal_rank"] == 1.0
