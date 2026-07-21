from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class ProductProductReader:
    """
    Reader for product.product

    Read-only access layer.
    """

    MODEL = "product.product"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        records = self.service.search_read(
            self.MODEL,
            [],
            fields=["id", "display_name"],
            limit=1,
        )
        return records[0] if records else None

    def by_id(self, record_id):
        records = self.service.read(
            self.MODEL,
            [record_id],
            fields=["id", "display_name"],
        )
        return records[0] if records else None

    def search(self, domain, fields=None, limit=100):
        if fields is None:
            fields = ["id", "display_name"]

        return self.service.search_read(
            self.MODEL,
            domain,
            fields=fields,
            limit=limit,
        )

    def all(self, fields=None, limit=100):
        return self.search(
            [],
            fields=fields,
            limit=limit,
        )
