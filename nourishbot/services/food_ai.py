"""High-level AI operations on food images and ingredient lists.

These functions hold the real logic behind the CrewAI tools. They have no
dependency on CrewAI or LangChain, so they can be reused from scripts,
notebooks or tests, and the tools in ``nourishbot.tools`` stay thin.
"""

from __future__ import annotations

from typing import List, Optional

from nourishbot import prompts
from nourishbot.services import watsonx_client as wx
from nourishbot.settings import get_settings
from nourishbot.utils.images import image_to_data_uri
from nourishbot.utils.text import parse_comma_separated


def _ask_vision_model(prompt: str, image_input: str) -> str:
    settings = get_settings()
    return wx.chat(
        model_id=settings.vision_model_id,
        content=[wx.text_part(prompt), wx.image_part(image_to_data_uri(image_input))],
        max_tokens=settings.vision_max_tokens,
    )


def extract_ingredients(image_input: str) -> str:
    """Ask the vision model which ingredients appear in the image (raw text reply)."""
    return _ask_vision_model(prompts.INGREDIENT_EXTRACTION_PROMPT, image_input)


def clean_ingredients(raw_ingredients: str) -> List[str]:
    """Turn a raw comma-separated ingredient string into a clean list."""
    return parse_comma_separated(raw_ingredients)


def filter_by_dietary_restrictions(
    ingredients: List[str], dietary_restrictions: Optional[str] = None
) -> List[str]:
    """Use the text LLM to keep only ingredients compatible with the restriction.

    If no restriction is given the list is returned unchanged (no model call).
    """
    if not dietary_restrictions:
        return ingredients

    settings = get_settings()
    reply = wx.chat(
        model_id=settings.text_model_id,
        content=[wx.text_part(prompts.build_dietary_filter_prompt(ingredients, dietary_restrictions))],
        max_tokens=settings.text_max_tokens,
    )
    return parse_comma_separated(reply)


def analyze_nutrition(image_input: str) -> str:
    """Ask the vision model for calories, nutrient breakdown and a health evaluation."""
    return _ask_vision_model(prompts.NUTRIENT_ANALYSIS_PROMPT, image_input)
