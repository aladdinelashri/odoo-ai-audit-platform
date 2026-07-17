from database.ai.ai_context import AIContext


class DatabaseFieldResolver:

    ORM_FIELD_MAPPING = {
        "display_name": "name",
        "complete_name": "name",
        "commercial_partner_id": "partner_id",
    }

    def __init__(self):
        self.context = AIContext()

    # ---------------------------------------------------------

    def resolve(self, model, field):

        self.context.initialize()

        if field in self.ORM_FIELD_MAPPING:

            candidate = self.ORM_FIELD_MAPPING[field]

            if candidate in self.context.fields(model):
                return candidate

        return field
