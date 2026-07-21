from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class POSConfigReader:
    """
    Reader for pos.config
    """

    MODEL = "pos.config"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        records = self.service.search_read(
            self.MODEL,
            [],
            fields=[
                "id",
                "name",
                "company_id",
                "picking_type_id",
                "journal_id",
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
                "company_id",
                "picking_type_id",
                "journal_id",
            ],
        )
        return records[0] if records else None

    def search(self, domain, fields=None, limit=100):

        if fields is None:
            fields = [
                "id",
                "name",
                "company_id",
                "picking_type_id",
                "journal_id",
            ]

        return self.service.search_read(
            self.MODEL,
            domain,
            fields=fields,
            limit=limit,
        )

    def all(self, fields=None, limit=100):
        return self.search([], fields=fields, limit=limit)
