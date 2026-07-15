"""
Result Formatter

Architecture V23

Converts raw PostgreSQL results into structured business objects.
"""

from __future__ import annotations


class ResultFormatter:

    def format(
        self,
        columns: list[str],
        rows: list[tuple],
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
