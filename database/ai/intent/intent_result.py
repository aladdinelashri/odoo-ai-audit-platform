"""
Intent Result

Architecture V6
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IntentResult:
    """
    Result returned by the intent classifier.
    """

    intent: str
    confidence: float = 1.0
