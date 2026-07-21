from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class BaseRepository:
    """
    Base repository for reusable business queries.
    """

    MODEL = None

    def __init__(self):
        self.service = XMLRPCObjectService()

    def search(self, domain=None, fields=None, limit=100, order=None):
        if domain is None:
            domain = []

        return self.service.search_read(
            self.MODEL,
            domain,
            fields=fields,
            limit=limit,
            order=order,
        )

    def read(self, ids, fields=None):
        return self.service.read(
            self.MODEL,
            ids,
            fields=fields,
        )

    def count(self, domain=None):
        if domain is None:
            domain = []

        return self.service.search_count(
            self.MODEL,
            domain,
        )
