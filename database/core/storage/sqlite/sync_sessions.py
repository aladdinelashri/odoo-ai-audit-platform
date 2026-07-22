from database.core.repositories.odoo.odoo_pos_session_repository import (
    OdooPOSSessionRepository,
)
from database.core.storage.sqlite.database import SQLiteDatabase


class SessionSynchronizer:

    def __init__(self):

        self.repo = OdooPOSSessionRepository()
        self.db = SQLiteDatabase()

    def sync(self):

        sessions = self.repo.all(limit=100000)

        rows = []

        for session in sessions:

            rows.append(
                (
                    session["id"],
                    session["config_id"][0]
                    if session.get("config_id")
                    else None,
                    session.get("name"),
                )
            )

        self.db.execute("DELETE FROM pos_sessions")

        self.db.executemany(
            """
            INSERT INTO pos_sessions
            (
                id,
                config_id,
                session_name
            )
            VALUES
            (
                ?,?,?
            )
            """,
            rows,
        )

        print(f"Sessions synchronized: {len(rows)}")

        return len(rows)


if __name__ == "__main__":

    SessionSynchronizer().sync()
