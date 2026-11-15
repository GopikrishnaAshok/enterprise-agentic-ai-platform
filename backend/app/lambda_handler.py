
import base64
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MAX_PROMPT_LENGTH = 4000


def response(status, payload):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(payload)
    }


def extract_answer(result):
    if isinstance(result, str):
        return result

    message = getattr(result, "message", None)

    if isinstance(message, dict):
        return "\n".join(
            item["text"]
            for item in message.get("content", [])
            if isinstance(item, dict)
            and isinstance(item.get("text"), str)
        )

    if isinstance(message, str):
        return message

    return str(result)


def lambda_handler(event, context):
    event = event or {}

    http = (
        event.get("requestContext", {})
        .get("http", {})
    )

    method = http.get("method", "")
    path = http.get("path", "")

    if method == "GET" and path.endswith("/health"):
        return response(200, {
            "status": "healthy",
            "service": "enterprise-agent-api"
        })

    if method != "POST" or not path.endswith("/agent"):
        return response(404, {
            "error": "Route not found"
        })

    try:
        body = event.get("body") or "{}"

        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")

        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, dict):
            return response(400, {
                "error": "Expected JSON object"
            })

        prompt = body.get("prompt")

        if not isinstance(prompt, str) or not prompt.strip():
            return response(400, {
                "error": "A non-empty prompt is required"
            })

        prompt = prompt.strip()

        if len(prompt) > MAX_PROMPT_LENGTH:
            return response(400, {
                "error": "Prompt exceeds maximum length"
            })

        lower_prompt = prompt.lower()

        if (
            lower_prompt.startswith("remember:")
            or lower_prompt in ("memory show", "memory clear")
        ):
            return response(501, {
                "error": "Cloud memory is not configured"
            })

        from backend.app.agents.agent import ask_agent

        result = ask_agent(prompt)

        return response(200, {
            "status": "success",
            "answer": extract_answer(result)
        })

    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return response(400, {
            "error": "Invalid request"
        })

    except Exception:
        logger.exception("Agent invocation failed")
        return response(500, {
            "error": "Agent execution failed"
        })
