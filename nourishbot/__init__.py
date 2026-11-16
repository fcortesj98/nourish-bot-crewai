"""AI NourishBot - a multi-agent, multimodal dietary assistant.

Based on the IBM Skills Network guided project "Building your own AI Nutrition
Coach using a Multi-Agent System and Multimodal AI" (IBM RAG and Agentic AI
Professional Certificate). See README.md for full credits.

Package layout (each layer only depends on the ones below it)::

    ui/ , cli.py        front-ends (Gradio web app, command line)
    workflows.py        choose crew -> kickoff -> format
    crews/              CrewAI agents, tasks and crews (+ YAML config)
    tools/              LangChain @tool wrappers exposed to agents
    services/           watsonx.ai client and food AI operations
    prompts.py, schemas.py, formatting.py, settings.py, utils/
"""

__version__ = "1.0.0"
