"""Base repository backed by SQLite cache."""

from database.core.storage.sqlite.sqlite_service import SQLiteService


class BaseRepository:
    """
    Base repository backed by SQLite cache.
    Translates Odoo-style domain/fields to SQLiteService query format.
    """

    TABLE = None

    def __init__(self):
        self.service = SQLiteService()

    def search(self, domain=None, fields=None, limit=None, order=None):
        """Search records matching domain."""
        return self.service.query(
            table=self.TABLE,
            columns=fields,
            conditions=domain,
            order_by=order,
            limit=limit,
        )

    def read(self, ids, fields=None):
        """Read records by IDs."""
        if not ids:
            return []
        id_list = ids if isinstance(ids, (list, tuple)) else [ids]
        return self.service.query(
            table=self.TABLE,
            columns=fields,
            conditions=[("id", "in", id_list)],
        )

    def count(self, domain=None):
        """Count records matching domain."""
        return self.service.count(
            table=self.TABLE,
            conditions=domain,
        )
