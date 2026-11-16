"""Small text-parsing helpers."""

from __future__ import annotations

from typing import List


def parse_comma_separated(raw: str) -> List[str]:
    """Split a comma-separated string into lower-cased, stripped, non-empty items."""
    return [item.strip().lower() for item in raw.split(",") if item.strip()]
