"""
Result Formatter

Production Engine V2
"""

from __future__ import annotations


class ResultFormatter:

    def format(self, rows: list[dict]) -> dict:

        return {
            "count": len(rows),
            "rows": rows,
        }
