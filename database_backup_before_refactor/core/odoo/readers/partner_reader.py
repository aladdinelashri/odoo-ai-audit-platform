from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class PartnerReader:
    """
    Reader for res.partner

    Read-only access layer.
    """

    MODEL = "res.partner"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        partners = self.service.search_read(
            self.MODEL,
            [],
            fields=["id", "name"],
            limit=1,
        )
        return partners[0] if partners else None

    def by_id(self, partner_id):
        partners = self.service.read(
            self.MODEL,
            [partner_id],
            fields=["id", "name"],
        )
        return partners[0] if partners else None

    def search(self, domain, fields=None, limit=100):
        if fields is None:
            fields = ["id", "name"]

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
