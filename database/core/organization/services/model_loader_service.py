from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class ModelLoaderService:

    def __init__(self):

        self.service = XMLRPCObjectService()

    def load(self, model, record_id, fields=None):

        records = self.service.search_read(
            model=model,
            domain=[
                ("id", "=", record_id),
            ],
            fields=fields,
            limit=1,
        )

        if not records:
            return None

        return records[0]
