"""
Pipeline Result

Architecture V3

Standard immutable result returned by the Core Pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineResult:
    """
    Final result produced by the Core Pipeline.
    """

    # ---------------------------------------------------------
    # Execution Status
    # ---------------------------------------------------------

    success: bool

    # ---------------------------------------------------------
    # Returned Data
    # ---------------------------------------------------------

    rows: list[dict[str, Any]] = field(default_factory=list)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    count: int = 0

    # ---------------------------------------------------------
    # Aggregate Result
    # ---------------------------------------------------------

    value: Any = None

    # ---------------------------------------------------------
    # Error Information
    # ---------------------------------------------------------

    error: str | None = None

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------

    @property
    def empty(self) -> bool:
        """
        Returns True when no rows are returned.
        """
        return self.count == 0

    # ---------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Convert result into a JSON-serializable dictionary.
        """

        result = {
            "success": self.success,
            "count": self.count,
            "rows": self.rows,
        }

        if self.value is not None:
            result["value"] = self.value

        if self.error:
            result["error"] = self.error

        if self.metadata:
            result["metadata"] = self.metadata

        return result
