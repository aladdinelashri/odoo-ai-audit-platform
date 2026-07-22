from database.core.repositories.odoo.odoo_pos_order_repository import (
    OdooPOSOrderRepository,
)
from database.core.storage.sqlite.database import SQLiteDatabase


class OrderSynchronizer:

    def __init__(self):

        self.repo = OdooPOSOrderRepository()
        self.db = SQLiteDatabase()

    def sync(self):

        orders = self.repo.all(limit=100000)

        rows = []

        for order in orders:

            rows.append(
                (
                    order["id"],
                    order["company_id"][0] if order.get("company_id") else None,
                    order["session_id"][0] if order.get("session_id") else None,
                    order["partner_id"][0] if order.get("partner_id") else None,
                    order.get("state"),
                    order.get("name"),
                    order.get("date_order"),
                    order.get("amount_total", 0.0),
                )
            )

        self.db.execute("DELETE FROM pos_orders")

        self.db.executemany(
            """
            INSERT INTO pos_orders
            (
                id,
                company_id,
                session_id,
                partner_id,
                state,
                order_name,
                order_date,
                amount_total
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?
            )
            """,
            rows,
        )

        return len(rows)


if __name__ == "__main__":

    total = OrderSynchronizer().sync()

    print(f"Orders synchronized: {total}")

