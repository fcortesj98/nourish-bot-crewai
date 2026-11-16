"""Shared agents and tasks for every NourishBot crew.

Agent personas and task descriptions live in ``crews/config/*.yaml``; this
module wires them to tools, output schemas and (optionally) a custom LLM.
Concrete crews in ``recipe_crew.py`` / ``analysis_crew.py`` choose which
agents and tasks to run.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from crewai import Agent, Task
from crewai.project import CrewBase, agent, task

from nourishbot.schemas import NutrientAnalysisOutput, RecipeSuggestionOutput
from nourishbot.settings import get_settings
from nourishbot.tools import (
    dietary_filter_tool,
    extract_ingredients_tool,
    filter_ingredients_tool,
    nutrient_analysis_tool,
)


@CrewBase
class BaseNourishBotCrew:
    """Defines every agent and task; subclasses assemble them into a ``Crew``.

    ``@CrewBase`` loads these YAML files (relative to this package) into
    ``self.agents_config`` / ``self.tasks_config`` dicts when the crew is created.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, image_data: str, dietary_restrictions: Optional[str] = None):
        self.image_data = image_data
        self.dietary_restrictions = dietary_restrictions

    # Helpers -----------------------------------------------------------------
    @staticmethod
    def _llm_kwargs() -> Dict[str, Any]:
        """Use ``NOURISHBOT_AGENT_LLM`` for agent reasoning if set, else CrewAI's default."""
        llm = get_settings().agent_llm
        return {"llm": llm} if llm else {}

    def _task_kwargs(self, name: str) -> Dict[str, Any]:
        config = self.tasks_config[name]
        return {"description": config["description"], "expected_output": config["expected_output"]}

    # Agents ------------------------------------------------------------------
    @agent
    def ingredient_detection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ingredient_detection_agent"],
            tools=[extract_ingredients_tool, filter_ingredients_tool],
            allow_delegation=False,
            max_iter=5,
            verbose=True,
            **self._llm_kwargs(),
        )

    @agent
    def dietary_filtering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["dietary_filtering_agent"],
            tools=[dietary_filter_tool],
            allow_delegation=True,
            max_iter=6,
            verbose=True,
            **self._llm_kwargs(),
        )

    @agent
    def nutrient_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["nutrient_analysis_agent"],
            tools=[nutrient_analysis_tool],
            allow_delegation=False,
            max_iter=4,
            verbose=True,
            **self._llm_kwargs(),
        )

    @agent
    def recipe_suggestion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recipe_suggestion_agent"],
            allow_delegation=False,
            verbose=True,
            **self._llm_kwargs(),
        )

    # Tasks -------------------------------------------------------------------
    # The crews run with Process.sequential, so CrewAI automatically passes the
    # outputs of earlier tasks to later ones (ingredients -> filter -> recipes).
    @task
    def ingredient_detection_task(self) -> Task:
        return Task(agent=self.ingredient_detection_agent(), **self._task_kwargs("ingredient_detection_task"))

    @task
    def dietary_filtering_task(self) -> Task:
        return Task(
            agent=self.dietary_filtering_agent(),
            **self._task_kwargs("dietary_filtering_task"),
        )

    @task
    def nutrient_analysis_task(self) -> Task:
        return Task(
            agent=self.nutrient_analysis_agent(),
            output_json=NutrientAnalysisOutput,
            **self._task_kwargs("nutrient_analysis_task"),
        )

    @task
    def recipe_suggestion_task(self) -> Task:
        return Task(
            agent=self.recipe_suggestion_agent(),
            output_json=RecipeSuggestionOutput,
            **self._task_kwargs("recipe_suggestion_task"),
        )
