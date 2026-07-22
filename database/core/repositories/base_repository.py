from database.core.storage.sqlite.sqlite_service import SQLiteService


class BaseRepository:
    """
    Base repository backed by SQLite cache.
    """

    TABLE = None

    def __init__(self):
        self.service = SQLiteService()

    def search(self, domain=None, fields=None, limit=None, order=None):

        return self.service.search(
            table=self.TABLE,
            domain=domain,
            fields=fields,
            limit=limit,
            order=order,
        )

    def read(self, ids, fields=None):

        return self.service.read(
            table=self.TABLE,
            ids=ids,
            fields=fields,
        )

    def count(self, domain=None):

        return self.service.count(
            table=self.TABLE,
            domain=domain,
        )
