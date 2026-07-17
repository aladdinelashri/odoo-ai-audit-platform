"""
Safe Executor

Architecture V11

Allows only read-only SQL statements.
"""

from __future__ import annotations


class SafeExecutor:

    READ_ONLY = {
        "SELECT",
        "WITH",
        "EXPLAIN",
    }

    BLOCKED = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
    }

    def validate(self, sql: str) -> bool:

        statement = sql.strip().upper()

        first_word = statement.split()[0]

        if first_word in self.BLOCKED:
            raise PermissionError(
                f"{first_word} statements are not allowed."
            )

        if first_word not in self.READ_ONLY:
            raise PermissionError(
                f"{first_word} is not allowed."
            )

        return True
