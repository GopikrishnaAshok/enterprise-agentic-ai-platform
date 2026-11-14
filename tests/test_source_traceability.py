from backend.app.evaluation.retrieval import parse_results, retrieve_evidence, format_evidence


class FakeClient:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def retrieve(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def test_source_extraction_and_deduplication():
    response = {"retrievalResults": [
        {"content": {"text": "Some evidence"}, "location": {"s3Location": {"uri": "s3://bucket/doc.pdf"}}},
        {"content": {"text": " Some   evidence "}, "location": {"s3Location": {"uri": "s3://bucket/doc.pdf"}}},
        {"content": {"text": "Some evidence"}, "location": {"s3Location": {"uri": "s3://bucket/other.pdf"}}},
        {"content": {"text": " "}},
    ]}
    client = FakeClient(response)
    evidence = retrieve_evidence(client, "KB1", "question")
    assert len(evidence) == 2
    assert evidence[0]["source_id"] == "s3://bucket/doc.pdf"
    assert evidence[0]["source_label"] == "doc.pdf"
    assert "SOURCE_NAME=doc.pdf" in format_evidence(evidence)
    assert client.calls[0]["retrievalConfiguration"]["managedSearchConfiguration"]["numberOfResults"] == 5


def test_unknown_source_does_not_crash():
    evidence = parse_results({"retrievalResults": [{"content": {"text": "Text"}}]})
    assert evidence[0]["source_id"] is None
    assert "SOURCE_ID=UNKNOWN" in format_evidence(evidence)


def test_empty_results():
    assert parse_results({}) == []
    assert format_evidence([]) == "SEARCH_STATUS=NO_DOCUMENT_CONTENT"


def test_retrieval_error_propagates():
    class BrokenClient:
        def retrieve(self, **kwargs):
            raise RuntimeError("simulated failure")
    import pytest
    with pytest.raises(RuntimeError, match="simulated failure"):
        retrieve_evidence(BrokenClient(), "KB", "question")
