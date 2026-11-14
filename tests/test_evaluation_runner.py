import pytest
from backend.app.evaluation.run_evaluation import evaluate_dataset


def test_offline_metrics_and_no_network():
    cases = [{"question": "Q1", "relevant_ids": ["s3://b/a"], "mock_results": [
        {"source_id": "s3://b/a"}, {"source_id": "s3://b/a"}, {"source_id": "s3://b/b"}]},
        {"question": "Q2", "relevant_ids": ["s3://b/c"], "mock_results": [
            {"source_id": "s3://b/b"}]}]
    report = evaluate_dataset(cases, k=2)
    assert report["mode"] == "offline_mock"
    assert report["question_count"] == 2
    assert report["results"][0]["retrieved_ids"] == ["s3://b/a", "s3://b/b"]
    assert report["averages"]["recall_at_k"] == .5
    assert report["averages"]["reciprocal_rank"] == .5
    assert report["averages"]["precision_at_k"] == .25


def test_missing_mock_data_rejected():
    with pytest.raises(ValueError, match="mock_results"):
        evaluate_dataset([{"question": "Q", "relevant_ids": ["a"]}])


def test_live_retriever_is_injected():
    calls = []
    def fake_retriever(question, k):
        calls.append((question, k))
        return [{"source_id": "a"}]
    report = evaluate_dataset([{"question": "Q", "relevant_ids": ["a"]}], retriever=fake_retriever)
    assert calls == [("Q", 5)]
    assert report["mode"] == "live"
