"""
Core Response Formatter

Architecture V3
"""

from __future__ import annotations

from database.core.pipeline.context import PipelineContext


class ResponseFormatter:
    """
    Architecture V3 Response Formatter.
    """

    # ---------------------------------------------------------

    def format(self, context: PipelineContext) -> dict:
        """
        Format execution results into the standard response structure.
        """

        rows = context.rows or []

        execution_plan = context.execution_plan or {}

        aggregate = execution_plan.get("aggregate")

        # ------------------------------------------------------------
        # Aggregate Result
        # ------------------------------------------------------------

        if aggregate:

            value = None

            if rows:

                value = next(iter(rows[0].values()))

            return {

                "success": True,

                "count": 1,

                "rows": rows,

                "value": value,

                "metadata": context.metadata,

            }

        # ------------------------------------------------------------
        # Standard Result
        # ------------------------------------------------------------

        return {

            "success": True,

            "count": len(rows),

            "rows": rows,

            "metadata": context.metadata,

        }
