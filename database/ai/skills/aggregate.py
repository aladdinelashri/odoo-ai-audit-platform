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

        lowered = text.lower()

        aggregate = None

        # -------------------------------------------------
        # Aggregate Function
        # -------------------------------------------------

        if any(

            word in lowered

            for word in (

                "sum",
                "total",
                "اجمالي",
                "إجمالي",
                "مجموع"

            )

        ):

            aggregate = "SUM"

        elif any(

            word in lowered

            for word in (

                "count",
                "عدد"

            )

        ):

            aggregate = "COUNT"

        elif any(

            word in lowered

            for word in (

                "average",
                "avg",
                "متوسط"

            )

        ):

            aggregate = "AVG"

        elif any(

            word in lowered

            for word in (

                "maximum",
                "max",
                "اعلى",
                "أعلى",
                "اكبر",
                "الأكبر"

            )

        ):

            aggregate = "MAX"

        elif any(

            word in lowered

            for word in (

                "minimum",
                "min",
                "اقل",
                "أقل",
                "اصغر",
                "الأصغر"

            )

        ):

            aggregate = "MIN"

        if not aggregate:

            return plan

        # -------------------------------------------------
        # Target Field
        # -------------------------------------------------

        if aggregate == "COUNT":

            field = "id"

        else:

            field = self.ranker.best(

                table,

                "monetary_total"

            )

            if not field:

                field = "id"

        # -------------------------------------------------

        plan["aggregate"] = {

            "function": aggregate,

            "field": field

        }

        return plan
