"""Centralised configuration for NourishBot.

Every value can be overridden with an environment variable (or a ``.env`` file
in the project root). The defaults reproduce the behaviour of the original
IBM Skills Network lab, where the Cloud IDE injects watsonx.ai credentials so
no API key is required.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

# Project layout --------------------------------------------------------------
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
EXAMPLES_DIR = PROJECT_ROOT / "examples"

# Load a .env file if python-dotenv is installed (it is in requirements.txt).
try:  # pragma: no cover - trivial import guard
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:  # pragma: no cover
    pass


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return an env var, treating empty strings as unset."""
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _env_int(name: str, default: int) -> int:
    value = _env(name)
    return int(value) if value is not None else default


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings."""

    # IBM watsonx.ai
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_api_key: Optional[str] = None
    watsonx_project_id: str = "skills-network"

    # Foundation models used by the tools
    vision_model_id: str = "meta-llama/llama-3-2-90b-vision-instruct"
    text_model_id: str = "ibm/granite-4-h-small"
    vision_max_tokens: int = 300
    text_max_tokens: int = 150

    # Optional LLM for the CrewAI agents' own reasoning (None = CrewAI default)
    agent_llm: Optional[str] = None

    # Networking
    image_download_timeout: int = 30
    server_host: str = "127.0.0.1"
    server_port: int = 5000

    @classmethod
    def from_env(cls) -> "Settings":
        defaults = cls()
        return cls(
            watsonx_url=_env("WATSONX_URL", defaults.watsonx_url),
            watsonx_api_key=_env("WATSONX_API_KEY", defaults.watsonx_api_key),
            watsonx_project_id=_env("WATSONX_PROJECT_ID", defaults.watsonx_project_id),
            vision_model_id=_env("NOURISHBOT_VISION_MODEL", defaults.vision_model_id),
            text_model_id=_env("NOURISHBOT_TEXT_MODEL", defaults.text_model_id),
            vision_max_tokens=_env_int("NOURISHBOT_VISION_MAX_TOKENS", defaults.vision_max_tokens),
            text_max_tokens=_env_int("NOURISHBOT_TEXT_MAX_TOKENS", defaults.text_max_tokens),
            agent_llm=_env("NOURISHBOT_AGENT_LLM", defaults.agent_llm),
            image_download_timeout=_env_int(
                "NOURISHBOT_IMAGE_TIMEOUT", defaults.image_download_timeout
            ),
            server_host=_env("NOURISHBOT_HOST", defaults.server_host),
            server_port=_env_int("NOURISHBOT_PORT", defaults.server_port),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings (read once from the environment)."""
    return Settings.from_env()
