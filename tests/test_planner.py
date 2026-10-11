
from backend.app.agents.planner import plan_request


def test_empty_request_is_rejected():
    result = plan_request("   ")

    assert result["intent"] == "invalid"
    assert result["steps"] == []


def test_document_list_request():
    result = plan_request("List available documents")

    assert result["intent"] == "list_documents"
    assert result["steps"][0]["tool"] == "list_s3_documents"


def test_document_question_uses_knowledge_base():
    result = plan_request(
        "According to the enterprise document, what investment is mentioned?"
    )

    assert result["intent"] == "document_question"
    assert result["steps"][0]["tool"] == "search_knowledge_base"


def test_document_analysis_and_roi_creates_two_steps():
    result = plan_request(
        "According to the AI investment document, "
        "if expected return is $20 million, calculate the ROI."
    )

    assert result["intent"] == "document_analysis_and_calculation"
    assert len(result["steps"]) == 2
    assert result["steps"][0]["tool"] == "search_knowledge_base"
    assert result["steps"][1]["tool"] == "calculate_business_metrics"
    assert result["steps"][1]["requires_verified_inputs"] is True


def test_general_request_leaves_decision_to_agent():
    result = plan_request("Explain what an AI agent is")

    assert result["intent"] == "general_request"
    assert result["steps"][0]["tool"] == "agent_decides"


def test_calculation_requires_verified_inputs():
    result = plan_request("Calculate ROI")

    assert result["intent"] == "business_calculation"
    assert result["steps"][0]["requires_verified_inputs"] is True

def test_calculation_plan_requires_both_verified_inputs():
    result = plan_request("Calculate ROI")

    step = result["steps"][0]

    assert step["required_inputs"] == [
        "investment",
        "expected_return",
    ]
    assert step["requires_verified_inputs"] is True
    assert step["do_not_invent_missing_inputs"] is True


def test_document_calculation_requires_evidence_and_verified_inputs():
    result = plan_request(
        "According to the report, calculate the ROI"
    )

    search_step, calculation_step = result["steps"]

    assert search_step["tool"] == "search_knowledge_base"
    assert search_step["evidence_required"] is True
    assert calculation_step["tool"] == "calculate_business_metrics"
    assert calculation_step["requires_verified_inputs"] is True
