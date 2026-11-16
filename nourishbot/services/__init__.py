"""Service layer: watsonx.ai access and the food-specific AI operations."""

from nourishbot.services.food_ai import (
    analyze_nutrition,
    clean_ingredients,
    extract_ingredients,
    filter_by_dietary_restrictions,
)

__all__ = [
    "analyze_nutrition",
    "clean_ingredients",
    "extract_ingredients",
    "filter_by_dietary_restrictions",
]
