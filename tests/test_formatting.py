from types import SimpleNamespace

from nourishbot.formatting import format_analysis_output, format_recipe_output

RECIPES = {
    "recipes": [
        {
            "title": "Veggie Stir Fry",
            "ingredients": ["broccoli", "carrot"],
            "instructions": "Stir fry everything.",
            "calorie_estimate": 350,
        }
    ]
}


def test_recipe_output_renders_each_recipe():
    md = format_recipe_output(RECIPES)
    assert md.startswith("## 🍽 Recipe Ideas")
    assert "### 1. Veggie Stir Fry" in md
    assert "| broccoli |" in md and "| carrot |" in md
    assert "**Calorie Estimate:** 350 kcal" in md


def test_recipe_output_reads_nested_task_output():
    nested = {"recipe_suggestion_task": SimpleNamespace(json_dict=RECIPES)}
    assert "Veggie Stir Fry" in format_recipe_output(nested)


def test_recipe_output_handles_empty():
    assert format_recipe_output({}).endswith("No recipes could be generated.")


def test_analysis_output_includes_tables_and_evaluation():
    md = format_analysis_output(
        {
            "dish": "Salmon bowl",
            "portion_size": "1 bowl",
            "estimated_calories": 520,
            "nutrients": {
                "protein": "35g",
                "carbohydrates": "40g",
                "fats": "18g",
                "vitamins": [{"name": "Vitamin D", "percentage_dv": "80%"}],
                "minerals": [{"name": "Iron", "amount": "3mg"}],
            },
            "health_evaluation": "Balanced meal.",
        }
    )
    assert "**Dish:** Salmon bowl" in md
    assert "| **Protein** | 35g |" in md
    assert "| Vitamin D | 80% |" in md
    assert "| Iron | 3mg |" in md
    assert md.rstrip().endswith("Balanced meal.")


def test_analysis_output_tolerates_missing_fields():
    md = format_analysis_output({"nutrients": None})
    assert "Nutrient Breakdown" in md
    assert "Vitamins" not in md
