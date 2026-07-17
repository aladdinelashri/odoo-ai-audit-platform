from sqlalchemy import text

from connectors.postgres.connection import PostgreSQLConnection


class BusinessDictionaryBuilder:

    def __init__(self):

        self.engine = PostgreSQLConnection().connect()

    # ---------------------------------------------------------

    def build(self):

        sql = """
        SELECT
            model,
            name
        FROM ir_model
        ORDER BY model
        """

        dictionary = {}

        with self.engine.connect() as conn:

            rows = conn.execute(text(sql)).mappings().all()

        for row in rows:

            model = row["model"]

            aliases = set()

            aliases.add(model.lower())

            aliases.add(model.replace(".", "_").lower())

            aliases.add(model.split(".")[-1].lower())

            name = row["name"]

            if isinstance(name, dict):

                for value in name.values():

                    if value:

                        aliases.add(value.strip().lower())

            elif name:

                aliases.add(str(name).strip().lower())

            dictionary[model] = sorted(aliases)

        return dictionary
