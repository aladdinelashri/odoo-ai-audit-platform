from database.core.repositories.odoo.odoo_pos_payment_repository import (
    OdooPOSPaymentRepository,
)
from database.core.storage.sqlite.database import SQLiteDatabase


class PaymentSynchronizer:

    def __init__(self):

        self.repo = OdooPOSPaymentRepository()
        self.db = SQLiteDatabase()

    def sync(self):

        payments = self.repo.all(limit=100000)

        rows = []

        for payment in payments:

            rows.append(
                (
                    payment["id"],
                    payment["pos_order_id"][0]
                    if payment.get("pos_order_id")
                    else None,
                    payment["session_id"][0]
                    if payment.get("session_id")
                    else None,
                    payment["payment_method_id"][1]
                    if payment.get("payment_method_id")
                    else None,
                    payment.get("amount", 0.0),
                )
            )

        self.db.execute("DELETE FROM pos_payments")

        self.db.executemany(
            """
            INSERT INTO pos_payments
            (
                id,
                order_id,
                session_id,
                payment_method,
                amount
            )
            VALUES
            (
                ?,?,?,?,?
            )
            """,
            rows,
        )

        print(f"Payments synchronized: {len(rows)}")

        return len(rows)


if __name__ == "__main__":

    PaymentSynchronizer().sync()
