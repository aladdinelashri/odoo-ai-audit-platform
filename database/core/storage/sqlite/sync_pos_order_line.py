# database/core/storage/sqlite/sync_pos_order_line.py

from database.core.odoo.readers.pos_order_line_reader import POSOrderLineReader
from database.core.storage.sqlite.database import SQLiteDatabase


class POSOrderLineSynchronizer:

    def __init__(self):

        self.reader = POSOrderLineReader()
        self.db = SQLiteDatabase()

    def sync(self):

        lines = self.reader.all(
            fields=[
                "id",
                "order_id",
                "product_id",
                "qty",
                "price_subtotal",
            ],
            limit=100000,
        )

        rows = []

        for line in lines:

            rows.append(
                (
                    line["id"],
                    line["order_id"][0] if line.get("order_id") else None,
                    line["product_id"][0] if line.get("product_id") else None,
                    line.get("qty", 0.0),
                    line.get("price_subtotal", 0.0),
                )
            )

        self.db.execute("DELETE FROM pos_order_lines")

        self.db.executemany(
            """
            INSERT INTO pos_order_lines
            (
                id,
                order_id,
                product_id,
                qty,
                price_subtotal
            )
            VALUES
            (
                ?,?,?,?,?
            )
            """,
            rows,
        )

        print(f"POS order lines synchronized: {len(rows)}")

        return len(rows)


if __name__ == "__main__":

    POSOrderLineSynchronizer().sync()
