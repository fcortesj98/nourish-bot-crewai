"""Analysis workflow: a single multimodal agent estimates calories and nutrients.

The vision model is capable enough to analyse the dish directly, so this crew
needs only one agent and one task.
"""

from __future__ import annotations

from crewai import Crew, Process
from crewai.project import CrewBase, crew

from nourishbot.crews.base import BaseNourishBotCrew


@CrewBase
class NourishBotAnalysisCrew(BaseNourishBotCrew):
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.nutrient_analysis_agent()],
            tasks=[self.nutrient_analysis_task()],
            process=Process.sequential,
            verbose=True,
        )
