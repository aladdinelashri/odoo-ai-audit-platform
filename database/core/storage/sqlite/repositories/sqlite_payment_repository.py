from database.core.storage.sqlite.database import SQLiteDatabase


class SQLitePaymentRepository:

    def __init__(self):

        self.db = SQLiteDatabase()

    def all(self):

        rows = self.db.query(
            """
            SELECT *
            FROM pos_payments
            ORDER BY id
            """
        )

        return [dict(row) for row in rows]
