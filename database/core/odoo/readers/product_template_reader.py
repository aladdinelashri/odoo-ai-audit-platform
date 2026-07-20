from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class ProductTemplateReader:
    """
    Reader for product.template

    Read-only access layer.
    """

    MODEL = "product.template"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        products = self.service.search_read(
            self.MODEL,
            [],
            fields=["id", "name"],
            limit=1,
        )
        return products[0] if products else None

    def by_id(self, product_id):
        products = self.service.read(
            self.MODEL,
            [product_id],
            fields=["id", "name"],
        )
        return products[0] if products else None

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
