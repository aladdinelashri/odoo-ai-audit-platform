import re

from database.ai.skills.base_skill import BaseSkill
from database.catalog.semantic_catalog import SemanticCatalog


class DateSkill(BaseSkill):

    def __init__(self):

        self.catalog = SemanticCatalog()

    # ---------------------------------------------------------

    def detect(self, text, plan):

        table = plan["table"]

        if not table:

            return []

        columns = self.catalog.columns(

            table,

            "document_date"

        )

        if not columns:

            return []

        field = columns[0]

        filters = []

        text = text.lower()

        if "today" in text or "اليوم" in text:

            filters.append(

                {

                    "field": field,

                    "operator": "=",

                    "value": "TODAY"

                }

            )

        elif "yesterday" in text or "أمس" in text:

            filters.append(

                {

                    "field": field,

                    "operator": "=",

                    "value": "YESTERDAY"

                }

            )

        return filters
