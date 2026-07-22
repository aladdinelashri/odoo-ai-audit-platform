from database.core.odoo.readers.pos_config_reader import POSConfigReader
from database.core.storage.sqlite.database import SQLiteDatabase


class POSConfigSynchronizer:

    def __init__(self):

        self.reader = POSConfigReader()
        self.db = SQLiteDatabase()

    def sync(self):

        configs = self.reader.all(
            fields=[
                "id",
                "name",
                "company_id",
                "iface_available_categ_ids",
            ],
            limit=1000,
        )

        rows = []

        for config in configs:

            rows.append(
                (
                    config["id"],
                    config["company_id"][0] if config["company_id"] else None,
                    config["name"],
                    ",".join(
                        str(x)
                        for x in config.get(
                            "iface_available_categ_ids",
                            [],
                        )
                    ),
                )
            )

        self.db.execute("DELETE FROM pos_configs")

        self.db.executemany(
            """
            INSERT INTO pos_configs
            (
                id,
                company_id,
                name,
                iface_available_categ_ids
            )
            VALUES
            (
                ?,?,?,?
            )
            """,
            rows,
        )

        return len(rows)


if __name__ == "__main__":

    total = POSConfigSynchronizer().sync()

    print(f"POS configs synchronized: {total}")
