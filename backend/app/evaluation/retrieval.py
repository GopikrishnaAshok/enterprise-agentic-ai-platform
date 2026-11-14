"""Source-aware Bedrock Knowledge Base retrieval. No AWS calls at import time."""
from pathlib import PurePosixPath
from urllib.parse import urlparse, unquote


def source_id(result: dict) -> str | None:
    """Return a stable document identifier from Bedrock location metadata."""
    location = result.get("location") or {}
    candidates = [
        (location.get("s3Location") or {}).get("uri"),
        (location.get("webLocation") or {}).get("url"),
        (location.get("confluenceLocation") or {}).get("url"),
        (location.get("salesforceLocation") or {}).get("url"),
        (location.get("sharePointLocation") or {}).get("url"),
        (result.get("metadata") or {}).get("x-amz-bedrock-kb-source-uri"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return None


def source_label(identifier: str | None) -> str:
    if not identifier:
        return "Unknown source"
    path = unquote(urlparse(identifier).path)
    return PurePosixPath(path).name or identifier


def parse_results(response: dict) -> list[dict]:
    """Deduplicate exact evidence from the same source, preserving ranked order."""
    evidence = []
    seen = set()
    for item in response.get("retrievalResults", []):
        content = item.get("content") or {}
        body = content.get("text")
        if not isinstance(body, str) or not body.strip():
            continue
        text = body.strip()
        identifier = source_id(item)
        key = (identifier, " ".join(text.split()))
        if key in seen:
            continue
        seen.add(key)
        evidence.append({"source_id": identifier, "source_label": source_label(identifier),
                         "text": text, "score": item.get("score")})
    return evidence


def retrieve_evidence(client, knowledge_base_id: str, query: str, limit: int = 5) -> list[dict]:
    if not query.strip():
        raise ValueError("Query must not be empty")
    if limit <= 0:
        raise ValueError("limit must be positive")
    response = client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={"text": query},
        retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": limit}},
    )
    return parse_results(response)


def format_evidence(evidence: list[dict]) -> str:
    if not evidence:
        return "SEARCH_STATUS=NO_DOCUMENT_CONTENT"
    parts = ["SEARCH_STATUS=SUCCESS", "SOURCE=Enterprise Knowledge Base"]
    for index, item in enumerate(evidence, 1):
        parts.append(f"--- DOCUMENT EVIDENCE {index} ---\n"
                     f"SOURCE_ID={item['source_id'] or 'UNKNOWN'}\n"
                     f"SOURCE_NAME={item['source_label']}\n"
                     f"{item['text']}")
    return "\n\n".join(parts)
