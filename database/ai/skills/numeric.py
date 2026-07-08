import re

from database.ai.skills.base_skill import BaseSkill
from database.catalog.field_ranker import FieldRanker


class NumericSkill(BaseSkill):

    def __init__(self):

        self.ranker = FieldRanker()

        self.patterns = [

            # English
            (">", r"greater than\s+(\d+)"),
            (">", r"more than\s+(\d+)"),
            (">", r"over\s+(\d+)"),
            (">", r"above\s+(\d+)"),

            ("<", r"less than\s+(\d+)"),
            ("<", r"under\s+(\d+)"),
            ("<", r"below\s+(\d+)"),

            ("=", r"equal(?:s)?\s+(\d+)"),

            # Arabic
            (">", r"أكبر من\s+(\d+)"),
            (">", r"أكثر من\s+(\d+)"),
            (">", r"يزيد عن\s+(\d+)"),
            (">", r"فوق\s+(\d+)"),

            ("<", r"أقل من\s+(\d+)"),
            ("<", r"أصغر من\s+(\d+)"),
            ("<", r"تحت\s+(\d+)"),

            ("=", r"يساوي\s+(\d+)")

        ]

    # ---------------------------------------------------------

    def detect(self, text, plan):

        table = plan.get("table")

        if not table:

            return []

        field = self.ranker.best(

            table,

            "monetary_total"

        )

        if not field:

            return []

        for operator, pattern in self.patterns:

            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )

            if match:

                return [

                    {

                        "field": field,

                        "operator": operator,

                        "value": int(

                            match.group(1)

                        )

                    }

                ]

        return []
