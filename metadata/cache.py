import json
from pathlib import Path

from metadata.schema import OdooSchema


class MetadataCache:

    def __init__(self):

        self.schema = OdooSchema()

        self.cache_dir = Path("database/schema")

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def file(self, table_name):

        return self.cache_dir / f"{table_name}.json"

    def build(self, table_name):

        columns = self.schema.columns(table_name)

        with open(
            self.file(table_name),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                columns,
                f,
                indent=4,
                ensure_ascii=False
            )

        return columns

    def load(self, table_name):

        file = self.file(table_name)

        if not file.exists():

            return self.build(table_name)

        with open(
            file,
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def refresh(self, table_name):

        return self.build(table_name)
