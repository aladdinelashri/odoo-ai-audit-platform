"""
Business Query Builder

Architecture V13

Builds a BusinessQuery from an existing QueryAnalyzer result.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery


class BusinessQueryBuilder:

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------

    def build(self, analysis: dict) -> BusinessQuery:

        return BusinessQuery(
            intent=analysis["intent"],
            confidence=analysis["confidence"],
            entities=analysis["entities"],
            aggregate=analysis["aggregate"],
            operator=analysis["operator"],
            value=analysis["value"],
            date=analysis["date"],
            raw_text=analysis.get("raw_text", ""),
        )
