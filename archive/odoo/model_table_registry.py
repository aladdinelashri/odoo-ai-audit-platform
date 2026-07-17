import re

from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class ModelTableRegistry:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

        self.registry = {}

    # ---------------------------------------------------------

    def build(self):

        sql = """
        SELECT
            model
        FROM ir_model
        ORDER BY model
        """

        with self.engine.connect() as conn:

            rows = conn.execute(text(sql)).mappings().all()

        registry = {}

        for row in rows:

            model = row["model"]

            table = model.replace(".", "_")

            registry[model] = {

                "model": model,

                "table": table

            }

        self.registry = registry

        return registry

    # ---------------------------------------------------------

    def table(self, model):

        if not self.registry:

            self.build()

        item = self.registry.get(model)

        if not item:

            return None

        return item["table"]

    # ---------------------------------------------------------

    def model(self, table):

        if not self.registry:

            self.build()

        for item in self.registry.values():

            if item["table"] == table:

                return item["model"]

        return None

    # ---------------------------------------------------------

    def all(self):

        if not self.registry:

            self.build()

        return self.registry
