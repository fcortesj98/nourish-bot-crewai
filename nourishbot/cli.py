"""Command-line interface: run a NourishBot workflow without the web UI.

Examples::

    python -m nourishbot examples/food-1.jpg recipe --diet vegan
    python -m nourishbot examples/food-2.jpg analysis
    python -m nourishbot https://example.com/meal.jpg analysis --json
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from nourishbot.workflows import FORMATTERS, WorkflowType, run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m nourishbot",
        description="AI NourishBot: recipe ideas or nutritional analysis from a food image.",
    )
    parser.add_argument("image", help="Path or http(s) URL of the food image.")
    parser.add_argument(
        "workflow",
        choices=[w.value for w in WorkflowType],
        help="'recipe' (ingredients -> diet filter -> recipes) or 'analysis' (nutrients & calories).",
    )
    parser.add_argument(
        "-d", "--diet", default="", help="Dietary restriction for the recipe workflow, e.g. vegan, keto."
    )
    parser.add_argument("--json", action="store_true", help="Print raw JSON instead of Markdown.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    workflow = WorkflowType.parse(args.workflow)

    output = run_workflow(args.image, workflow, args.diet)
    if args.json:
        print(json.dumps(output, indent=2, default=str))
    else:
        print(FORMATTERS[workflow](output))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
