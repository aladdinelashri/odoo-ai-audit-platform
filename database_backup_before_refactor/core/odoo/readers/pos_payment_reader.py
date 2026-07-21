from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class POSPaymentReader:
    """
    Reader for pos.payment

    Read-only access layer.
    """

    MODEL = "pos.payment"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        records = self.service.search_read(
            self.MODEL,
            [],
            fields=[
                "id",
                "pos_order_id",
                "payment_method_id",
                "amount",
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
                "pos_order_id",
                "payment_method_id",
                "amount",
            ],
        )
        return records[0] if records else None

    def search(self, domain, fields=None, limit=100):
        if fields is None:
            fields = [
                "id",
                "pos_order_id",
                "payment_method_id",
                "amount",
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
