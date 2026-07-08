from database.ai.skills.base_skill import BaseSkill
from database.catalog.field_ranker import FieldRanker


class AggregateSkill(BaseSkill):

    def __init__(self):

        self.ranker = FieldRanker()

    # ---------------------------------------------------------

    def detect(self, text, plan):

        table = plan["table"]

        if not table:

            return plan

        text = text.lower()

        aggregate = None

        if any(word in text for word in [

            "sum",
            "total",
            "اجمالي",
            "إجمالي",
            "مجموع"

        ]):

            aggregate = "SUM"

        elif any(word in text for word in [

            "count",
            "عدد"

        ]):

            aggregate = "COUNT"

        if not aggregate:

            return plan

        field = self.ranker.best(

            table,

            "monetary_total"

        )

        if aggregate == "COUNT":

            field = "id"

        plan["aggregate"] = {

            "function": aggregate,

            "field": field

        }

        return plan
