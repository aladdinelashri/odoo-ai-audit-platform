from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class POSOrderLineReader:
    """
    Reader for pos.order.line

    Read-only access layer.
    """

    MODEL = "pos.order.line"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        records = self.service.search_read(
            self.MODEL,
            [],
            fields=["id", "order_id", "product_id", "qty", "price_subtotal"],
            limit=1,
        )
        return records[0] if records else None

    def by_id(self, record_id):
        records = self.service.read(
            self.MODEL,
            [record_id],
            fields=["id", "order_id", "product_id", "qty", "price_subtotal"],
        )
        return records[0] if records else None

    def search(self, domain, fields=None, limit=100):
        if fields is None:
            fields = [
                "id",
                "order_id",
                "product_id",
                "qty",
                "price_subtotal",
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
