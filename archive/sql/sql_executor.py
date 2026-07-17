from database.sql.connection import DatabaseConnection


class SQLExecutor:

    def __init__(self):

        self.db = DatabaseConnection()
        self.cursor = None

    # ---------------------------------------------------------

    def execute(self, sql, params=None):

        self.cursor = self.db.cursor()

        self.cursor.execute(sql, params or ())

        columns = [c[0] for c in self.cursor.description]

        rows = self.cursor.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    # ---------------------------------------------------------

    def close(self):

        if self.cursor is not None:
            self.cursor.close()

        self.db.close()
