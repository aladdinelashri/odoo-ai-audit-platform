from database.sql.connection import DatabaseConnection


class SQLExecutor:

    def __init__(self):

        self.db = DatabaseConnection()

    # ---------------------------------------------------------

    def execute(self, sql, params=None):

        cursor = self.db.cursor()

        cursor.execute(sql, params or ())

        rows = cursor.fetchall()

        cursor.close()

        return rows
