
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MAX_PROMPT_LENGTH = 4000


def lambda_handler(event, context):
    """Handle API Gateway HTTP API requests."""

    request_context = event.get("requestContext") or {}
    http_context = request_context.get("http") or {}
    method = http_context.get("method", "")

    if method != "POST":
        return respond(405, {"error": "Method not allowed"})

    try:
        body = event.get("body") or "{}"

        if event.get("isBase64Encoded"):
            import base64
            body = base64.b64decode(body).decode("utf-8")

        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, dict):
            return respond(400, {"error": "JSON object required"})

        prompt = body.get("prompt")

        if not isinstance(prompt, str) or not prompt.strip():
            return respond(400, {"error": "A prompt is required"})

        if len(prompt) > MAX_PROMPT_LENGTH:
            return respond(400, {"error": "Prompt is too long"})

        # File-based memory is not persistent in Lambda.
        # Block these commands until persistent storage is configured.
        if prompt.strip().lower().startswith("remember:") or \
           prompt.strip().lower() in ("memory show", "memory clear"):
            return respond(
                501,
                {"error": "Persistent memory is not configured"}
            )

        from backend.app.agents.agent import ask_agent

        result = ask_agent(prompt.strip())

        # Strands returns an AgentResult for normal requests.
        answer = getattr(result, "message", None)

        if isinstance(answer, dict):
            blocks = answer.get("content", [])
            answer = "\n".join(
                block.get("text", "")
                for block in blocks
                if isinstance(block, dict) and "text" in block
            )

        if not isinstance(answer, str):
            answer = str(result)

        return respond(200, {
            "status": "success",
            "answer": answer
        })

    except (ValueError, json.JSONDecodeError):
        return respond(400, {"error": "Invalid JSON request"})

    except Exception:
        logger.exception("Agent invocation failed")
        return respond(500, {"error": "Agent execution failed"})


def respond(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
