"""
SQL Validator

Architecture V19
"""

from __future__ import annotations


class SQLValidator:

    BLOCKED = {
        "DELETE",
        "UPDATE",
        "INSERT",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
    }

    # ---------------------------------------------------------

    def validate(self, sql: str) -> bool:

        statement = sql.strip().upper()

        if not statement.startswith("SELECT"):
            return False

        for keyword in self.BLOCKED:
            if keyword in statement:
                return False

        return True
