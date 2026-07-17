"""
Core SQL Validator

Architecture V3

Ensures that generated SQL is safe before execution.
"""

from __future__ import annotations

import re

from database.core.pipeline.context import PipelineContext


class SQLValidator:
    """
    Architecture V3 SQL Validator.
    """

    FORBIDDEN = (
        "insert",
        "update",
        "delete",
        "drop",
        "truncate",
        "alter",
        "create",
        "grant",
        "revoke",
    )

    # ------------------------------------------------------------------

    def validate(self, context: PipelineContext) -> None:
        """
        Validate SQL before execution.
        """

        sql = context.sql

        if not sql:
            raise ValueError("Empty SQL statement.")

        lowered = sql.lower()

        # ------------------------------------------------------------
        # Forbidden statements
        # ------------------------------------------------------------

        for keyword in self.FORBIDDEN:

            if re.search(rf"\b{keyword}\b", lowered):

                raise ValueError(
                    f"Forbidden SQL statement: {keyword.upper()}"
                )

        # ------------------------------------------------------------
        # Multiple statements
        # ------------------------------------------------------------

        if sql.count(";") > 0:

            raise ValueError(
                "Multiple SQL statements are not allowed."
            )

        # ------------------------------------------------------------
        # SELECT only
        # ------------------------------------------------------------

        if not lowered.strip().startswith("select"):

            raise ValueError(
                "Only SELECT statements are allowed."
            )

        # ------------------------------------------------------------
        # Passed validation
        # ------------------------------------------------------------

        context.add_metadata(
            "sql_validation",
            "passed",
        )
