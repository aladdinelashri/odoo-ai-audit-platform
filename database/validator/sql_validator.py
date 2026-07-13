import re


class SQLValidator:

    def __init__(self):

        self.allowed_tables = set()

        self.allowed_columns = set()

    # ---------------------------------------------------------

    def allow_tables(self, tables):

        self.allowed_tables = {

            table.lower()

            for table in tables

        }

    # ---------------------------------------------------------

    def allow_columns(self, columns):

        self.allowed_columns = {

            column.lower()

            for column in columns

        }

    # ---------------------------------------------------------

    def validate(self, sql):

        if not sql:

            raise Exception("Empty SQL")

        normalized = sql.lower()

        # -------------------------------------------------
        # Dangerous Statements
        # -------------------------------------------------

        forbidden = [

            "insert",

            "update",

            "delete",

            "drop",

            "truncate",

            "alter",

            "create",

            "grant",

            "revoke"

        ]

        for keyword in forbidden:

            if re.search(

                rf"\b{keyword}\b",

                normalized

            ):

                raise Exception(

                    f"Forbidden SQL statement : {keyword}"

                )

        # -------------------------------------------------
        # Multiple Statements
        # -------------------------------------------------

        if normalized.count(";") > 0:

            raise Exception(

                "Multiple SQL statements are not allowed."

            )

        # -------------------------------------------------
        # FROM TABLE
        # -------------------------------------------------

        match = re.search(

            r"from\s+([a-zA-Z0-9_]+)",

            normalized

        )

        if match:

            table = match.group(1)

            if (

                self.allowed_tables

                and

                table not in self.allowed_tables

            ):

                raise Exception(

                    f"Table not allowed : {table}"

                )

        return True
