from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class FieldRegistry:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()
        self.registry = {}

    # ---------------------------------------------------------

    def build(self):

        sql = """
        SELECT
            m.model,
            f.name,
            f.field_description,
            f.ttype,
            f.relation
        FROM ir_model_fields f
        JOIN ir_model m
            ON m.id = f.model_id
        ORDER BY m.model, f.name
        """

        with self.engine.connect() as conn:

            rows = conn.execute(text(sql)).mappings().all()

        registry = {}

        for row in rows:

            model = row["model"]

            registry.setdefault(model, {})

            registry[model][row["name"]] = {
                "name": row["name"],
                "label": row["field_description"],
                "type": row["ttype"],
                "relation": row["relation"],
            }

        self.registry = registry

        return registry

    # ---------------------------------------------------------

    def fields(self, model):

        if not self.registry:
            self.build()

        return self.registry.get(model, {})

    # ---------------------------------------------------------

    def get_fields(self, model):

        return list(self.fields(model).keys())

    # ---------------------------------------------------------

    def field(self, model, field):

        if not self.registry:
            self.build()

        return self.registry.get(model, {}).get(field)

    # ---------------------------------------------------------

    def exists(self, model, field):

        return self.field(model, field) is not None
