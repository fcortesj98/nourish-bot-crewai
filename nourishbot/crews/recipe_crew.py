"""Recipe workflow: detect ingredients -> apply dietary filter -> suggest recipes."""

from __future__ import annotations

from crewai import Crew, Process
from crewai.project import CrewBase, crew

from nourishbot.crews.base import BaseNourishBotCrew


@CrewBase
class NourishBotRecipeCrew(BaseNourishBotCrew):
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.ingredient_detection_agent(),
                self.dietary_filtering_agent(),
                self.recipe_suggestion_agent(),
            ],
            tasks=[
                self.ingredient_detection_task(),
                self.dietary_filtering_task(),
                self.recipe_suggestion_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )
