"""Tools used by the dietary filtering agent."""

from __future__ import annotations

from typing import List, Optional

from langchain.tools import tool

from nourishbot.services import food_ai


@tool("Filter based on dietary restrictions")
def dietary_filter_tool(ingredients: List[str], dietary_restrictions: Optional[str] = None) -> List[str]:
    """
    Uses an LLM model to filter ingredients based on dietary restrictions.

    :param ingredients: List of ingredients.
    :param dietary_restrictions: Dietary restrictions (e.g., vegan, gluten-free). Defaults to None.
    :return: Filtered list of ingredients that comply with the dietary restrictions.
    """
    return food_ai.filter_by_dietary_restrictions(ingredients, dietary_restrictions)
