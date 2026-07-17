"""
Intent Classifier

Architecture V6
"""

from __future__ import annotations

from database.ai.intent.intent_result import IntentResult


class IntentClassifier:

    def __init__(self) -> None:

        self._rules = {

            "SHOW": [
                "show",
                "display",
                "find",
                "get",
            ],

            "LIST": [
                "list",
            ],

            "COUNT": [
                "count",
                "how many",
                "number of",
            ],

            "SUM": [
                "sum",
                "total",
            ],

            "AVERAGE": [
                "average",
                "avg",
                "mean",
            ],

            "MIN": [
                "minimum",
                "min",
                "lowest",
                "smallest",
            ],

            "MAX": [
                "maximum",
                "max",
                "highest",
                "largest",
            ],
        }

    # ---------------------------------------------------------

    def classify(self, text: str) -> IntentResult:

        query = text.lower().strip()

        for intent, keywords in self._rules.items():

            for keyword in keywords:

                if keyword in query:

                    return IntentResult(
                        intent=intent,
                        confidence=1.0,
                    )

        return IntentResult(
            intent="UNKNOWN",
            confidence=0.0,
        )
