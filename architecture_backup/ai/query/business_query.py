"""
Business Query

Architecture V8
"""

from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass(slots=True)
class BusinessQuery:
    """
    Canonical business query.
    """

    # Intent
    intent: str = "UNKNOWN"
    confidence: float = 0.0

    # Entity
    entities: list[str] = dataclasses.field(default_factory=list)
    aggregate: str | None = None

    # Filter
    field: str | None = None
    operator: str | None = None
    value: Any = None
    date: str | None = None

    # Diagnostics
    raw_text: str = ""
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)
