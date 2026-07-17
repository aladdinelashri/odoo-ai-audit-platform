"""
Result Summary

Architecture V12

Creates a simple summary of formatted query results.
"""

from __future__ import annotations


class ResultSummary:

    def summarize(self, rows: list[dict]) -> dict:

        return {
            "count": len(rows),
            "empty": len(rows) == 0,
        }
