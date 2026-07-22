from database.core.cache.cache_manager import CacheManager
from database.core.storage.sqlite.database import SQLiteDatabase


class SessionBusinessUnitSynchronizer:

    def __init__(self):

        self.cache = CacheManager().build()
        self.db = SQLiteDatabase()

    def sync(self):

        rows = []

        for session in self.cache.sessions.values():

            config_id = session["config_id"]

            config_record = self.cache.configs.get(config_id)

            if not config_record:
                continue

            categories = config_record.get(
                "iface_available_categ_ids",
                [],
            )

            if not categories:
                continue

            rows.append(
                (
                    session["id"],
                    categories[0],
                )
            )

        self.db.execute("DELETE FROM session_business_units")

        self.db.executemany(
            """
            INSERT INTO session_business_units
            VALUES (?,?)
            """,
            rows,
        )

        return len(rows)
