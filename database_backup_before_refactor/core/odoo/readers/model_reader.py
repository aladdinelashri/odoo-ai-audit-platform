from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class ModelReader:
    """
    Reader for Odoo models.
    """

    def __init__(self):
        self.service = XMLRPCObjectService()

    def all(self):
        return self.service.search_read(
            model="ir.model",
            domain=[],
            fields=[
                "id",
                "model",
                "name",
                "state",
            ],
        )

    def first(self):
        models = self.service.search_read(
            model="ir.model",
            domain=[],
            fields=[
                "id",
                "model",
                "name",
                "state",
            ],
            limit=1,
        )

        if models:
            return models[0]

        return None

    def by_model(self, model_name):
        models = self.service.search_read(
            model="ir.model",
            domain=[
                ("model", "=", model_name),
            ],
            fields=[
                "id",
                "model",
                "name",
                "state",
            ],
            limit=1,
        )

        if models:
            return models[0]

        return None
