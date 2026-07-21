from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class StockMoveReader:
    """
    Reader for stock.move

    Read-only access layer.
    """

    MODEL = "stock.move"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        records = self.service.search_read(
            self.MODEL,
            [],
            fields=[
                "id",
                "name",
                "product_id",
                "product_uom_qty",
                "state",
            ],
            limit=1,
        )
        return records[0] if records else None

    def by_id(self, record_id):
        records = self.service.read(
            self.MODEL,
            [record_id],
            fields=[
                "id",
                "name",
                "product_id",
                "product_uom_qty",
                "state",
            ],
        )
        return records[0] if records else None

    def search(self, domain, fields=None, limit=100):
        if fields is None:
            fields = [
                "id",
                "name",
                "product_id",
                "product_uom_qty",
                "state",
            ]

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
