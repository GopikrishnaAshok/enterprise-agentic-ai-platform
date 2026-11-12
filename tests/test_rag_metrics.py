
"""Tests for RAG retrieval evaluation metrics."""

import pytest

from backend.app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_precision_at_k():
    retrieved = ["doc1", "doc2", "doc3"]
    relevant = {"doc1", "doc3"}

    assert precision_at_k(
        retrieved, relevant, 3
    ) == pytest.approx(2 / 3)


def test_recall_at_k():
    retrieved = ["doc1", "doc2", "doc3"]
    relevant = {"doc1", "doc3", "doc4"}

    assert recall_at_k(
        retrieved, relevant, 3
    ) == pytest.approx(2 / 3)


def test_reciprocal_rank():
    retrieved = ["doc1", "doc2", "doc3"]
    relevant = {"doc3"}

    assert reciprocal_rank(
        retrieved, relevant
    ) == pytest.approx(1 / 3)


def test_precision_empty_results():
    assert precision_at_k(
        [], {"doc1"}, 5
    ) == 0.0


def test_recall_empty_relevant_set():
    assert recall_at_k(
        ["doc1"], set(), 5
    ) == 0.0


def test_reciprocal_rank_no_match():
    assert reciprocal_rank(
        ["doc1", "doc2"], {"doc3"}
    ) == 0.0


def test_invalid_k():
    with pytest.raises(ValueError):
        precision_at_k(["doc1"], {"doc1"}, 0)

    with pytest.raises(ValueError):
        recall_at_k(["doc1"], {"doc1"}, 0)


def test_precision_top_k():
    retrieved = ["doc1", "doc2", "doc3"]
    relevant = {"doc3"}

    assert precision_at_k(
        retrieved, relevant, 2
    ) == 0.0


def test_recall_top_k():
    retrieved = ["doc1", "doc2", "doc3"]
    relevant = {"doc1", "doc3"}

    assert recall_at_k(
        retrieved, relevant, 2
    ) == 0.5


def test_first_result_relevant():
    assert reciprocal_rank(
        ["doc1", "doc2"], {"doc1"}
    ) == 1.0
