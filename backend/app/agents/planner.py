
"""Lightweight, deterministic planner for the enterprise AI agent."""

from typing import Any


def _step(
    tool: str,
    purpose: str,
    **requirements: Any,
) -> dict[str, Any]:
    """Create a consistent, serializable plan step."""
    return {
        "tool": tool,
        "purpose": purpose,
        **requirements,
    }


def plan_request(prompt: str) -> dict[str, Any]:
    """Create an execution plan without calling an AI model.

    This function classifies requests and describes safety requirements.
    It does not execute tools or verify document evidence.
    """

    request = prompt.strip().lower()

    if not request:
        return {
            "intent": "invalid",
            "steps": [],
            "message": "Request cannot be empty.",
        }

    list_phrases = (
        "list documents",
        "available documents",
        "what documents",
        "list files",
        "documents are available",
    )

    wants_document_list = any(
        phrase in request for phrase in list_phrases
    )

    calculation_phrases = (
        "roi",
        "return on investment",
        "net benefit",
        "calculate the return",
        "calculate return",
    )

    wants_calculation = any(
        phrase in request for phrase in calculation_phrases
    )

    document_phrases = (
        "document",
        "knowledge base",
        "according to",
        "based on the report",
        "based on the data",
        "enterprise data",
    )

    wants_document_evidence = any(
        phrase in request for phrase in document_phrases
    )

    if wants_document_list:
        return {
            "intent": "list_documents",
            "steps": [
                _step(
                    "list_s3_documents",
                    "List documents in the enterprise repository.",
                )
            ],
        }

    if wants_calculation and wants_document_evidence:
        return {
            "intent": "document_analysis_and_calculation",
            "steps": [
                _step(
                    "search_knowledge_base",
                    "Retrieve evidence and identify relevant figures.",
                    evidence_required=True,
                ),
                _step(
                    "calculate_business_metrics",
                    "Calculate ROI and net benefit using verified values.",
                    requires_verified_inputs=True,
                    required_inputs=["investment", "expected_return"],
                    do_not_invent_missing_inputs=True,
                ),
            ],
        }

    if wants_calculation:
        return {
            "intent": "business_calculation",
            "steps": [
                _step(
                    "calculate_business_metrics",
                    "Calculate ROI and net benefit.",
                    requires_verified_inputs=True,
                    required_inputs=["investment", "expected_return"],
                    do_not_invent_missing_inputs=True,
                )
            ],
        }

    if wants_document_evidence:
        return {
            "intent": "document_question",
            "steps": [
                _step(
                    "search_knowledge_base",
                    "Retrieve evidence relevant to the request.",
                    evidence_required=True,
                )
            ],
        }

    return {
        "intent": "general_request",
        "steps": [
            _step(
                "agent_decides",
                "Let the existing Strands agent determine the next action.",
            )
        ],
    }
