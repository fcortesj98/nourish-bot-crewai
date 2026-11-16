"""Gradio web interface for NourishBot."""

from __future__ import annotations

import logging
import os

import gradio as gr

from nourishbot.formatting import NO_RESULTS_PLACEHOLDER
from nourishbot.ui.assets import CSS, EXAMPLES, INSTRUCTIONS, JS
from nourishbot.utils.images import save_pil_image_to_temp
from nourishbot.workflows import WorkflowType, run_workflow_markdown

logger = logging.getLogger(__name__)


def analyze_food(image, dietary_restrictions, workflow_type, progress=gr.Progress(track_tqdm=True)):
    """Gradio callback: run the selected workflow on the uploaded image.

    :param image: Uploaded image (PIL format).
    :param dietary_restrictions: Optional restriction, e.g. "vegan".
    :param workflow_type: "recipe" or "analysis".
    :return: Markdown shown in the results panel.
    """
    if image is None:
        raise gr.Error("Please upload an image (or pick an example) first.")
    if not workflow_type:
        raise gr.Error("Please select a workflow type: 'recipe' or 'analysis'.")
    try:
        workflow = WorkflowType.parse(workflow_type)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc

    image_path = save_pil_image_to_temp(image)
    try:
        return run_workflow_markdown(image_path, workflow, dietary_restrictions)
    except Exception as exc:  # surface failures in the UI instead of a blank panel
        logger.exception("Workflow '%s' failed", workflow.value)
        raise gr.Error(f"The {workflow.value} workflow failed: {exc}") from exc
    finally:
        try:
            os.remove(image_path)
        except OSError:
            pass


def build_demo() -> gr.Blocks:
    """Build (but do not launch) the Gradio Blocks app."""
    with gr.Blocks(theme=gr.themes.Citrus(), css=CSS, js=JS) as demo:
        gr.Markdown("# How it works", elem_classes="title")
        for line in INSTRUCTIONS:
            gr.Markdown(line, elem_classes="text")

        with gr.Row():
            with gr.Column(scale=1, min_width=400):
                gr.Markdown("## Inputs", elem_classes="title")
                image_input = gr.Image(type="pil", label="Upload Image")
                dietary_input = gr.Textbox(label="Dietary Restrictions (optional)", placeholder="e.g., vegan")
                workflow_radio = gr.Radio([w.value for w in WorkflowType], label="Workflow Type")
                submit_btn = gr.Button("Analyze")

            with gr.Column(scale=2, min_width=600):
                # Examples only autofill the inputs; the user still clicks Analyze.
                gr.Examples(
                    examples=EXAMPLES,
                    inputs=[image_input, dietary_input, workflow_radio],
                    label="Try an Example: Select one of the examples below to autofill the input section then click Analyze",
                )
                gr.Markdown("## Results will appear here...", elem_classes="title")
                result_display = gr.Markdown(NO_RESULTS_PLACEHOLDER, height=500)

        submit_btn.click(
            fn=analyze_food,
            inputs=[image_input, dietary_input, workflow_radio],
            outputs=result_display,
        )

    return demo
