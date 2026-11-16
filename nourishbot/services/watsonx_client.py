"""Thin wrapper around the IBM watsonx.ai SDK.

The original lab created ``Credentials``/``APIClient`` objects at import time in
two different modules. Here they are created lazily, exactly once, and every
model call goes through :func:`chat`, so swapping a model or provider only
requires touching this file (or the environment variables in ``settings``).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List

from nourishbot.settings import get_settings

ContentPart = Dict[str, Any]


@lru_cache(maxsize=1)
def get_credentials():
    """Build watsonx.ai credentials from settings.

    In the Skills Network Cloud IDE no API key is needed; elsewhere set
    ``WATSONX_API_KEY`` (and usually ``WATSONX_PROJECT_ID``).
    """
    from ibm_watsonx_ai import Credentials

    settings = get_settings()
    kwargs = {"url": settings.watsonx_url}
    if settings.watsonx_api_key:
        kwargs["api_key"] = settings.watsonx_api_key
    return Credentials(**kwargs)


@lru_cache(maxsize=8)
def get_model(model_id: str, max_tokens: int):
    """Return a cached ``ModelInference`` for the given model and token limit."""
    from ibm_watsonx_ai.foundation_models import ModelInference

    return ModelInference(
        model_id=model_id,
        credentials=get_credentials(),
        project_id=get_settings().watsonx_project_id,
        params={"max_tokens": max_tokens},
    )


def chat(model_id: str, content: List[ContentPart], max_tokens: int) -> str:
    """Send a single user message (text and/or image parts) and return the reply text."""
    model = get_model(model_id, max_tokens)
    response = model.chat(messages=[{"role": "user", "content": content}])
    return response["choices"][0]["message"]["content"]


def text_part(text: str) -> ContentPart:
    return {"type": "text", "text": text}


def image_part(data_uri: str) -> ContentPart:
    return {"type": "image_url", "image_url": {"url": data_uri}}
