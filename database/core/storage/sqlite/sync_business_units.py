from database.core.odoo.readers.pos_category_reader import POSCategoryReader
from database.core.storage.sqlite.database import SQLiteDatabase


class BusinessUnitSynchronizer:

    def __init__(self):

        self.reader = POSCategoryReader()
        self.db = SQLiteDatabase()

    def sync(self):

        categories = self.reader.all(
            fields=[
                "id",
                "name",
            ],
            limit=1000,
        )

        business_units = []

        for category in categories:

            business_units.append(
                (
                    category["id"],
                    str(category["id"]),
                    category["name"],
                    "pos.category",
                )
            )

        self.db.execute("DELETE FROM business_units")

        self.db.executemany(
            """
            INSERT INTO business_units
            (
                id,
                code,
                name,
                source
            )
            VALUES
            (
                ?,?,?,?
            )
            """,
            business_units,
        )

        sessions = self.db.query(
            """
            SELECT
                id,
                config_id
            FROM pos_sessions
            """
        )

        configs = {
            row["id"]: row
            for row in self.db.query(
                """
                SELECT
                    id,
                    iface_available_categ_ids
                FROM pos_configs
                """
            )
        }

        mappings = []

        for session in sessions:

            config = configs.get(session["config_id"])

            if not config:
                continue

            categories = config["iface_available_categ_ids"]

            if not categories:
                continue

            first_category = int(categories.split(",")[0])

            mappings.append(
                (
                    session["id"],
                    first_category,
                )
            )

        self.db.execute("DELETE FROM session_business_units")

        self.db.executemany(
            """
            INSERT INTO session_business_units
            (
                session_id,
                business_unit_id
            )
            VALUES
            (
                ?,?
            )
            """,
            mappings,
        )

        print(f"Business units synchronized: {len(business_units)}")
        print(f"Session business units synchronized: {len(mappings)}")

        return len(mappings)


if __name__ == "__main__":

    BusinessUnitSynchronizer().sync()
