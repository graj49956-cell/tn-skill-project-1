from __future__ import annotations

import re
import time
from functools import lru_cache
from typing import TypeVar, Type

from google import genai
from google.genai import types
from pydantic import BaseModel

from .config import get_settings


T = TypeVar("T", bound=BaseModel)


class GeminiServiceError(RuntimeError):
    """Raised when Gemini cannot complete a request."""


@lru_cache
def get_client() -> genai.Client:
    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. "
            "Please add it to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def _is_quota_error(exc: Exception) -> bool:
    message = str(exc).upper()

    return (
        "429" in message
        or "RESOURCE_EXHAUSTED" in message
        or "RATE LIMIT" in message
        or "QUOTA EXCEEDED" in message
        or "TOO_MANY_REQUESTS" in message
    )


def _quota_error_message(exc: Exception) -> str:
    message = str(exc)

    match = re.search(
        r"retry in\s+([0-9]+(?:\.[0-9]+)?)s",
        message,
        re.IGNORECASE,
    )

    if match:
        seconds = int(float(match.group(1)))

        return (
            "Gemini API rate limit reached. "
            f"Please wait about {seconds} seconds and try again. "
            "If your daily Free Tier quota is exhausted, "
            "you must wait for the quota reset or use a project "
            "with available Gemini quota."
        )

    return (
        "Gemini API quota has been exceeded. "
        "Please wait for the quota to reset or use a Gemini "
        "API project with available quota."
    )


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    settings = get_settings()
    client = get_client()

    last_error: Exception | None = None

    for attempt in range(settings.gemini_max_retries + 1):

        try:

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = response.text

            if text and text.strip():
                return text.strip()

            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        except Exception as exc:

            if _is_quota_error(exc):
                raise GeminiServiceError(
                    _quota_error_message(exc)
                ) from exc

            last_error = exc

            if attempt < settings.gemini_max_retries:
                time.sleep(1.5 * (attempt + 1))

    raise GeminiServiceError(
        f"Gemini request failed: {last_error}"
    ) from last_error


def generate_structured(
    prompt: str,
    schema: Type[T],
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1800,
) -> T:

    settings = get_settings()
    client = get_client()

    last_error: Exception | None = None

    for attempt in range(settings.gemini_max_retries + 1):

        try:

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                response_mime_type="application/json",
                response_schema=schema,
            )

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            if response.parsed is not None:
                return response.parsed

            text = response.text

            if text and text.strip():
                return schema.model_validate_json(text)

            raise GeminiServiceError(
                "Gemini returned an empty structured response."
            )

        except Exception as exc:

            if _is_quota_error(exc):
                raise GeminiServiceError(
                    _quota_error_message(exc)
                ) from exc

            last_error = exc

            if attempt < settings.gemini_max_retries:
                time.sleep(1.5 * (attempt + 1))

    raise GeminiServiceError(
        f"Gemini structured-output request failed: {last_error}"
    ) from last_error