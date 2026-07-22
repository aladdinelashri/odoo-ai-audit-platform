from database.core.storage.sqlite.database import SQLiteDatabase


class SQLiteOrderRepository:

    def __init__(self):

        self.db = SQLiteDatabase()

    def all(self):

        rows = self.db.query(
            """
            SELECT *
            FROM pos_orders
            ORDER BY id
            """
        )

        return [dict(row) for row in rows]

    def by_id(self, order_id):

        row = self.db.query_one(
            """
            SELECT *
            FROM pos_orders
            WHERE id = ?
            """,
            (order_id,),
        )

        if row is None:
            return None

        return dict(row)
