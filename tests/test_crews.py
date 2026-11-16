"""Check crew wiring offline (agents, tasks, tools) without calling any model."""

import pytest

pytest.importorskip("crewai")


@pytest.fixture(autouse=True)
def _dummy_llm_key(monkeypatch):
    # CrewAI's default LLM needs a key to be *constructed*; nothing is called.
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")


def test_recipe_crew_wiring():
    from nourishbot.crews import NourishBotRecipeCrew

    crew = NourishBotRecipeCrew(image_data="x.jpg", dietary_restrictions="vegan").crew()
    roles = [a.role.strip() for a in crew.agents]
    assert roles == ["Vision AI Specialist", "Nutritionist AI Specialist", "Recipe Generation Specialist"]
    assert len(crew.tasks) == 3
    assert crew.tasks[-1].output_json.__name__ == "RecipeSuggestionOutput"
    tool_names = {t.name for t in crew.agents[0].tools}
    assert {"Extract ingredients", "Filter ingredients"} <= tool_names


def test_analysis_crew_wiring():
    from nourishbot.crews import NourishBotAnalysisCrew

    crew = NourishBotAnalysisCrew(image_data="x.jpg").crew()
    assert [a.role.strip() for a in crew.agents] == ["Nutrition Analysis Specialist"]
    assert crew.tasks[0].output_json.__name__ == "NutrientAnalysisOutput"
