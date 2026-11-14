"""Offline-by-default RAG evaluation runner.

Dataset JSON: [{"question": "...", "relevant_ids": ["s3://bucket/doc.pdf"],
                "mock_results": [{"source_id": "s3://bucket/doc.pdf", "text": "..."}]}]
Without --live, every question MUST supply mock_results.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.evaluation.rag_evaluator import evaluate_retrieval
from backend.app.evaluation.retrieval import parse_results


def evaluate_dataset(cases: list[dict], k: int = 5, retriever=None) -> dict:
    if not cases:
        raise ValueError("Evaluation dataset cannot be empty")
    if k <= 0:
        raise ValueError("k must be positive")
    rows = []
    for index, case in enumerate(cases, 1):
        question = case.get("question", "")
        relevant = case.get("relevant_ids")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"Case {index}: question is required")
        if not isinstance(relevant, list) or not relevant or not all(isinstance(x, str) and x for x in relevant):
            raise ValueError(f"Case {index}: nonempty relevant_ids list required")
        if retriever is None:
            if "mock_results" not in case:
                raise ValueError(f"Case {index}: mock_results required in offline mode")
            raw = case["mock_results"]
            if not isinstance(raw, list):
                raise ValueError(f"Case {index}: mock_results must be a list")
            evidence = [{"source_id": item.get("source_id"), "text": item.get("text", "")}
                        for item in raw]
        else:
            evidence = retriever(question, k)
        # Multiple chunks from one source count as one document in document-level metrics.
        ids = list(dict.fromkeys(item["source_id"] for item in evidence if item.get("source_id")))
        metrics = evaluate_retrieval(ids, set(relevant), k)
        rows.append({"question": question, "retrieved_ids": ids, "relevant_ids": relevant, **metrics})
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "live" if retriever else "offline_mock",
        "k": k,
        "question_count": len(rows),
        "averages": {key: sum(row[key] for row in rows) / len(rows)
                     for key in ("precision_at_k", "recall_at_k", "reciprocal_rank")},
        "results": rows,
    }


def main():
    parser = argparse.ArgumentParser(description="RAG retrieval evaluation")
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--output", default="reports/rag_evaluation.json", type=Path)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--live", action="store_true", help="Explicitly allow paid AWS retrieval requests")
    parser.add_argument("--kb-id", help="Bedrock Knowledge Base ID (required with --live)")
    parser.add_argument("--region", default="us-east-1")
    args = parser.parse_args()
    cases = json.loads(args.dataset.read_text(encoding="utf-8"))
    retriever = None
    if args.live:
        if not args.kb_id:
            parser.error("--kb-id is required with --live")
        import boto3
        from backend.app.evaluation.retrieval import retrieve_evidence
        client = boto3.client("bedrock-agent-runtime", region_name=args.region)
        retriever = lambda question, k: retrieve_evidence(client, args.kb_id, question, k)
    report = evaluate_dataset(cases, args.k, retriever)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"{report['mode']}: {report['question_count']} questions; averages={report['averages']}")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
