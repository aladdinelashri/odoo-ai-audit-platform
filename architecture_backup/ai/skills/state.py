from database.ai.skills.base_skill import BaseSkill
from database.catalog.semantic_catalog import SemanticCatalog


class StateSkill(BaseSkill):

    def __init__(self):

        self.catalog = SemanticCatalog()

    # ---------------------------------------------------------

    def detect(self, text, plan):

        table = plan["table"]

        if not table:

            return []

        columns = self.catalog.columns(

            table,

            "document_state"

        )

        if not columns:

            return []

        field = columns[0]

        text = text.lower()

        mapping = {

            "posted": "posted",

            "draft": "draft",

            "cancelled": "cancel",

            "canceled": "cancel",

            "مرحل": "posted",

            "مرحل": "posted",

            "مسودة": "draft",

            "ملغي": "cancel",

            "ملغى": "cancel"

        }

        filters = []

        for word, value in mapping.items():

            if word in text:

                filters.append(

                    {

                        "field": field,

                        "operator": "=",

                        "value": value

                    }

                )

                break

        return filters
