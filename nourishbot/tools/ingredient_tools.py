"""Tools used by the ingredient detection agent."""

from __future__ import annotations

from typing import List

from langchain.tools import tool

from nourishbot.services import food_ai


@tool("Extract ingredients")
def extract_ingredients_tool(image_input: str):
    """
    Extract ingredients from a food item image.

    :param image_input: The image file path (local) or URL (remote).
    :return: A list of ingredients extracted from the image.
    """
    return food_ai.extract_ingredients(image_input)


@tool("Filter ingredients")
def filter_ingredients_tool(raw_ingredients: str) -> List[str]:
    """
    Processes the raw ingredient data and filters out non-food items or noise.

    :param raw_ingredients: Raw ingredients as a string.
    :return: A list of cleaned and relevant ingredients.
    """
    return food_ai.clean_ingredients(raw_ingredients)
