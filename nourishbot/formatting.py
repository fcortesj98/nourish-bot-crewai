"""Render workflow outputs (dicts) as Markdown for the Gradio UI and the CLI."""

from __future__ import annotations

from typing import Any, Dict, List

NO_RESULTS_PLACEHOLDER = (
    "<div style='border: 1px solid #ccc; "
    "padding: 1rem; text-align: center; "
    "color: #666;'>No results yet</div>"
)


def _extract_recipes(final_output: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find the recipe list in a crew output dict (top level or nested task output)."""
    if "recipes" in final_output:
        return final_output["recipes"]
    task_output = final_output.get("recipe_suggestion_task")
    if task_output is not None and getattr(task_output, "json_dict", None):
        return task_output.json_dict.get("recipes", [])
    return []


def format_recipe_output(final_output: Dict[str, Any]) -> str:
    """Format the recipe workflow output as Markdown (one section per recipe)."""
    output = "## 🍽 Recipe Ideas\n\n"
    recipes = _extract_recipes(final_output)

    if not recipes:
        return output + "No recipes could be generated."

    for idx, recipe in enumerate(recipes, 1):
        output += f"### {idx}. {recipe['title']}\n\n"

        output += "**Ingredients:**\n"
        output += "| Ingredient |\n"
        output += "|------------|\n"
        for ingredient in recipe["ingredients"]:
            output += f"| {ingredient} |\n"
        output += "\n"

        output += f"**Instructions:**\n{recipe['instructions']}\n\n"
        output += f"**Calorie Estimate:** {recipe['calorie_estimate']} kcal\n\n"
        output += "---\n\n"

    return output


def _table(headers: tuple, rows: List[tuple], separators: tuple) -> str:
    out = "| " + " | ".join(headers) + " |\n"
    out += "|" + "|".join(separators) + "|\n"
    for row in rows:
        out += "| " + " | ".join(str(cell) for cell in row) + " |\n"
    return out


def format_analysis_output(final_output: Dict[str, Any]) -> str:
    """Format the nutritional analysis output as Markdown tables + health evaluation."""
    output = "## 🥗 Nutritional Analysis\n\n"

    # Basic dish information
    if dish := final_output.get("dish"):
        output += f"**Dish:** {dish}\n\n"
    if portion := final_output.get("portion_size"):
        output += f"**Portion Size:** {portion}\n\n"
    if est_cal := final_output.get("estimated_calories"):
        output += f"**Estimated Calories:** {est_cal} calories\n\n"
    if total_cal := final_output.get("total_calories"):
        output += f"**Total Calories:** {total_cal} calories\n\n"

    nutrients = final_output.get("nutrients") or {}

    # Macronutrients
    output += "**Nutrient Breakdown:**\n\n"
    output += "| **Nutrient**       | **Amount** |\n"
    output += "|--------------------|------------|\n"
    for macro in ("protein", "carbohydrates", "fats"):
        if value := nutrients.get(macro):
            output += f"| **{macro.capitalize()}** | {value} |\n"

    # Vitamins
    if vitamins := nutrients.get("vitamins") or []:
        output += "\n**Vitamins:**\n\n"
        output += _table(
            ("**Vitamin**", "**%DV**"),
            [(v.get("name", "N/A"), v.get("percentage_dv", "N/A")) for v in vitamins],
            ("-------------", "--------"),
        )

    # Minerals
    if minerals := nutrients.get("minerals") or []:
        output += "\n**Minerals:**\n\n"
        output += _table(
            ("**Mineral**", "**Amount**"),
            [(m.get("name", "N/A"), m.get("amount", "N/A")) for m in minerals],
            ("-------------", "-----------"),
        )

    # Health evaluation last
    if health_eval := final_output.get("health_evaluation"):
        output += "\n**Health Evaluation:**\n\n"
        output += health_eval + "\n"

    return output
