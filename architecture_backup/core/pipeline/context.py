"""
Pipeline Context

Architecture V3

This object carries all information generated during a single
query execution.

Each pipeline stage reads from the context and appends its own
output without modifying previous stages.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineContext:
    """
    Shared context passed across the entire execution pipeline.
    """

    # ------------------------------------------------------------------
    # Original user input
    # ------------------------------------------------------------------

    query: str

    # ------------------------------------------------------------------
    # AI Layer
    # ------------------------------------------------------------------

    parsed: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Planning Layer
    # ------------------------------------------------------------------

    execution_plan: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # SQL Layer
    # ------------------------------------------------------------------

    sql: str | None = None

    sql_parameters: tuple[Any, ...] = field(default_factory=tuple)

    # ------------------------------------------------------------------
    # Execution Layer
    # ------------------------------------------------------------------

    rows: list[dict[str, Any]] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Response Layer
    # ------------------------------------------------------------------

    response: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    success: bool = True

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------

    def fail(self, message: str) -> None:
        """
        Mark pipeline as failed.
        """

        self.success = False
        self.error = message

    # ------------------------------------------------------------------

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Store diagnostic metadata.
        """

        self.metadata[key] = value

    # ------------------------------------------------------------------

    @property
    def has_error(self) -> bool:
        """
        Returns True if pipeline execution failed.
        """

        return not self.success
