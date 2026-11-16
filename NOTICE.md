# NOTICE

This project is a refactored derivative of course material from the **IBM Skills Network**
guided project *"Building your own AI Nutrition Coach using a Multi-Agent System and
Multimodal AI"*, part of the **IBM RAG and Agentic AI Professional Certificate**.

- Original code base: IBM Developer Skills Network on GitHub
  (https://github.com/ibm-developer-skills-network), branch `5-final` used by the lab.
  Earlier public version: https://github.com/HaileyTQuach/Smart-Nutritional-App
- Original author: Hailey Quach
- Lab contributors: Ricky Shi, Karan Goswami, Wojciech "Victor" Fulmyk
- Lab content license: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)

The agent and task definitions (`nourishbot/crews/config/*.yaml`), the prompts
(`nourishbot/prompts.py`), the output schemas, the formatters and the Gradio UI
come from the original lab code. The modular package structure, settings layer,
CLI, tests and documentation were added in this refactor.
