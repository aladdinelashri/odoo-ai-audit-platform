import json
from pathlib import Path

from database.schema.sql_builder import SQLBuilder


class ReportGenerator:

    def __init__(self):

        self.sql = SQLBuilder()

        self.output = Path("reporting/generated")

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate(self, metadata):

        sql = self.sql.build(

            base_table=metadata["base_table"],

            joins=metadata.get("joins"),

            columns=metadata["columns"],

            where=metadata.get("where"),

            order=metadata.get("order"),

            limit=metadata.get("limit")

        )

        file = self.output / f"{metadata['id']}.sql"

        file.write_text(

            sql,

            encoding="utf-8"

        )

        return sql
