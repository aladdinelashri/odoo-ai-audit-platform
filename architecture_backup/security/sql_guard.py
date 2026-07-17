"""
SQL Guard

Architecture V21
"""

from __future__ import annotations

import re

from database.security.sql_validator import SQLValidator
from database.security.schema_validator import SchemaValidator


class SQLGuard:

    def __init__(
        self,
        sql_validator: SQLValidator,
        schema_validator: SchemaValidator,
    ) -> None:

        self.sql_validator = sql_validator
        self.schema_validator = schema_validator

    # ---------------------------------------------------------

    def validate(
        self,
        model: str,
        sql: str,
    ) -> bool:

        if not self.sql_validator.validate(sql):
            return False

        if not self.schema_validator.table_exists(model):
            return False

        columns = re.findall(
            r"SELECT\s+(.*?)\s+FROM",
            sql,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not columns:
            return False

        selected = columns[0].strip()

        if selected == "*":
            return True

        for column in [c.strip() for c in selected.split(",")]:

            if not self.schema_validator.column_exists(
                model,
                column,
            ):
                return False

        return True
