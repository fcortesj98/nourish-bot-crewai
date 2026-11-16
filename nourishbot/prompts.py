"""Prompt templates sent to the watsonx.ai foundation models.

Kept verbatim from the original IBM Skills Network lab code so model behaviour
is unchanged; they now live in one place so they are easy to tune.
"""

from __future__ import annotations

from typing import Iterable

INGREDIENT_EXTRACTION_PROMPT = "Extract ingredients from the food item image"

DIETARY_FILTER_PROMPT_TEMPLATE = """
        You are an AI nutritionist specialized in dietary restrictions. 
        Given the following list of ingredients: {ingredients}, 
        and the dietary restriction: {dietary_restrictions}, 
        remove any ingredient that does not comply with this restriction. 
        Return only the compliant ingredients as a comma-separated list with no additional commentary.
        """

NUTRIENT_ANALYSIS_PROMPT = """
            You are an expert nutritionist. Your task is to analyze the food items displayed in the image and provide a detailed nutritional assessment using the following format:
        1. **Identification**: List each identified food item clearly, one per line.
        2. **Portion Size & Calorie Estimation**: For each identified food item, specify the portion size and provide an estimated number of calories. Use bullet points with the following structure:
        - **[Food Item]**: [Portion Size], [Number of Calories] calories
        Example:
        *   **Salmon**: 6 ounces, 210 calories
        *   **Asparagus**: 3 spears, 25 calories
        3. **Total Calories**: Provide the total number of calories for all food items.
        Example:
        Total Calories: [Number of Calories]
        4. **Nutrient Breakdown**: Include a breakdown of key nutrients such as **Protein**, **Carbohydrates**, **Fats**, **Vitamins**, and **Minerals**. Use bullet points, and for each nutrient provide details about the contribution of each food item.
        Example:
        *   **Protein**: Salmon (35g), Asparagus (3g), Tomatoes (1g) = [Total Protein]
        5. **Health Evaluation**: Evaluate the healthiness of the meal in one paragraph.
        6. **Disclaimer**: Include the following exact text as a disclaimer:
        The nutritional information and calorie estimates provided are approximate and are based on general food data. 
        Actual values may vary depending on factors such as portion size, specific ingredients, preparation methods, and individual variations. 
        For precise dietary advice or medical guidance, consult a qualified nutritionist or healthcare provider.
        Format your response exactly like the template above to ensure consistency.
        """


def build_dietary_filter_prompt(ingredients: Iterable[str], dietary_restrictions: str) -> str:
    return DIETARY_FILTER_PROMPT_TEMPLATE.format(
        ingredients=", ".join(ingredients),
        dietary_restrictions=dietary_restrictions,
    )
