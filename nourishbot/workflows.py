"""Workflow orchestration: pick the right crew, run it, format the result.

This is the single entry point used by both the Gradio UI and the CLI, so the
two front-ends can never drift apart.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, Optional

from nourishbot.formatting import format_analysis_output, format_recipe_output


class WorkflowType(str, Enum):
    """The two workflows offered by NourishBot."""

    RECIPE = "recipe"  # detect ingredients -> diet filter -> recipes
    ANALYSIS = "analysis"  # calories + nutrients + health evaluation

    @classmethod
    def parse(cls, value: "str | WorkflowType") -> "WorkflowType":
        try:
            return cls(str(getattr(value, "value", value)).strip().lower())
        except ValueError as exc:
            choices = " or ".join(f"'{w.value}'" for w in cls)
            raise ValueError(f"Invalid workflow type {value!r}. Choose {choices}.") from exc


FORMATTERS: Dict[WorkflowType, Callable[[Dict[str, Any]], str]] = {
    WorkflowType.RECIPE: format_recipe_output,
    WorkflowType.ANALYSIS: format_analysis_output,
}


def build_crew(workflow: WorkflowType, image_path: str, dietary_restrictions: Optional[str] = None):
    """Instantiate the CrewAI crew for a workflow (imported lazily: CrewAI is heavy)."""
    from nourishbot.crews import NourishBotAnalysisCrew, NourishBotRecipeCrew

    if workflow is WorkflowType.RECIPE:
        return NourishBotRecipeCrew(image_data=image_path, dietary_restrictions=dietary_restrictions)
    return NourishBotAnalysisCrew(image_data=image_path)


def run_workflow(
    image_path: str,
    workflow_type: "str | WorkflowType",
    dietary_restrictions: Optional[str] = None,
) -> Dict[str, Any]:
    """Run a workflow on an image and return the crew's structured output as a dict."""
    workflow = WorkflowType.parse(workflow_type)
    dietary_restrictions = (dietary_restrictions or "").strip()

    inputs = {
        "uploaded_image": image_path,
        "dietary_restrictions": dietary_restrictions,
        "workflow_type": workflow.value,
    }
    crew_instance = build_crew(workflow, image_path, dietary_restrictions or None)
    result = crew_instance.crew().kickoff(inputs=inputs)
    return result.to_dict()


def run_workflow_markdown(
    image_path: str,
    workflow_type: "str | WorkflowType",
    dietary_restrictions: Optional[str] = None,
) -> str:
    """Run a workflow and return the result rendered as Markdown."""
    workflow = WorkflowType.parse(workflow_type)
    output = run_workflow(image_path, workflow, dietary_restrictions)
    return FORMATTERS[workflow](output)
