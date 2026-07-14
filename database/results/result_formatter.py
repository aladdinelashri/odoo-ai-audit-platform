"""
Result Formatter

Architecture V12

Converts raw PostgreSQL rows into a structured result object.
"""

from __future__ import annotations

from typing import Any


class ResultFormatter:

    def format(
        self,
        columns: list[str],
        rows: list[tuple[Any, ...]],
    ) -> list[dict]:

        result: list[dict] = []

        for row in rows:
            result.append(
                dict(zip(columns, row))
            )

        return result
