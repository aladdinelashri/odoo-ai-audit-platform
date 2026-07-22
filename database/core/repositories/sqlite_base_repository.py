import sqlite3
from database.core.config.settings import Settings


class SQLiteBaseRepository:

    TABLE = None

    def __init__(self):

        settings = Settings()

        self.conn = sqlite3.connect(settings.sqlite_db_path)
        self.conn.row_factory = sqlite3.Row

    def all(self):

        cur = self.conn.execute(f"SELECT * FROM {self.TABLE}")
        return [dict(r) for r in cur.fetchall()]

    def by_id(self, record_id):

        cur = self.conn.execute(
            f"SELECT * FROM {self.TABLE} WHERE id=?",
            (record_id,),
        )

        row = cur.fetchone()

        return dict(row) if row else None
