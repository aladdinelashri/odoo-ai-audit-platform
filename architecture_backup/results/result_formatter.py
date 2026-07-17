"""
Result Formatter

Architecture V23

Converts raw PostgreSQL rows into a structured result object.
"""

from __future__ import annotations

from typing import Any


class ResultFormatter:

    def format(
        self,
        columns: list[str],
        rows: list[tuple[Any, ...]],
    ) -> dict:

        records = []

        for row in rows:
            records.append(
                dict(zip(columns, row))
            )

        return {
            "columns": columns,
            "rows": records,
            "count": len(records),
        }
