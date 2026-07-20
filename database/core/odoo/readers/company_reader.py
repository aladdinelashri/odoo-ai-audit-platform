from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class CompanyReader:

    def __init__(self):
        self.service = XMLRPCObjectService()

    def all(self):
        return self.service.search_read(
            model="res.company",
            domain=[],
            fields=[
                "id",
                "name",
            ],
        )

    def first(self):
        companies = self.service.search_read(
            model="res.company",
            domain=[],
            fields=[
                "id",
                "name",
            ],
            limit=1,
        )

        if companies:
            return companies[0]

        return None
