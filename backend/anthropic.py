from httpx import AsyncClient
import json
from os import environ

TIMEOUT_SECONDS = 45
API_KEY = environ.get("ANTHROPIC_API_KEY")


class ClaudeError(Exception):
    usage = None

    def __init__(self, message, usage=None):
        super().__init__(message)
        self.usage = usage


class APIStatusError(ClaudeError):
    pass


class RateLimitError(ClaudeError):
    pass


class BadRequestError(ClaudeError):
    pass


class UnknownError(ClaudeError):
    pass


class ClaudeTimeoutError(ClaudeError):
    pass


async def claude_request_json(
    messages: list[str],
    model="claude-3-5-sonnet-20241022",
    temperature=1.0,
) -> dict:
    if not messages:
        raise ValueError("No messages provided")

    prepared_messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": message} for message in messages],
        },
        {
            "role": "assistant",
            "content": "{",
        },
    ]

    async with AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": API_KEY,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "prompt-caching-2024-07-31",
            },
            json={
                "model": model,
                "messages": prepared_messages,
                "max_tokens": 2048,
                "temperature": temperature,
            },
            timeout=TIMEOUT_SECONDS,
        )

    try:
        result = response.json()
        usage = result.get("usage")
    except json.JSONDecodeError:
        result = None

    if response.status_code == 429:
        raise RateLimitError(f"Rate limit exceeded: {response.text}", usage=usage)
    elif response.status_code == 400:
        raise BadRequestError(f"Bad request: {response.text}", usage=usage)
    elif response.status_code >= 500:
        raise APIStatusError(f"API error: {response.text}", usage=usage)
    elif response.status_code != 200:
        raise UnknownError(f"Unexpected response: {response.text}", usage=usage)

    if result.get("type") == "error":
        raise ClaudeError(result["error"]["message"], usage=usage)

    result_json = json.loads("{" + result["content"][0]["text"], strict=False)

    return result_json
