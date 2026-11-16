"""Tools used by the nutrient analysis agent."""

from __future__ import annotations

from langchain.tools import tool

from nourishbot.services import food_ai


@tool("Analyze nutritional values and calories of the dish from uploaded image")
def nutrient_analysis_tool(image_input: str):
    """
    Provide a detailed nutrient breakdown and estimate the total calories of all ingredients from the uploaded image.

    :param image_input: The image file path (local) or URL (remote).
    :return: A string with nutrient breakdown (protein, carbs, fat, etc.) and estimated calorie information.
    """
    return food_ai.analyze_nutrition(image_input)
