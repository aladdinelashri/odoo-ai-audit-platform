import re


class ParameterDetector:

    def detect(self, text):

        result = {

            "limit": None,

            "order": "DESC",

            "aggregate": None

        }

        lowered = text.lower()

        # -------------------------------------------------
        # LIMIT
        # -------------------------------------------------

        m = re.search(

            r"(?:last|آخر)\s+(\d+)",

            text,

            re.IGNORECASE

        )

        if m:

            result["limit"] = int(m.group(1))

            result["order"] = "DESC"

        m = re.search(

            r"(?:first|أول)\s+(\d+)",

            text,

            re.IGNORECASE

        )

        if m:

            result["limit"] = int(m.group(1))

            result["order"] = "ASC"

        # -------------------------------------------------
        # AGGREGATE
        # -------------------------------------------------

        if any(

            word in lowered

            for word in (

                "sum",
                "total",
                "إجمالي",
                "مجموع"

            )

        ):

            result["aggregate"] = "SUM"

        elif any(

            word in lowered

            for word in (

                "count",
                "عدد"

            )

        ):

            result["aggregate"] = "COUNT"

        elif any(

            word in lowered

            for word in (

                "average",
                "avg",
                "متوسط"

            )

        ):

            result["aggregate"] = "AVG"

        elif any(

            word in lowered

            for word in (

                "maximum",
                "max",
                "أعلى",
                "اكبر",
                "الأكبر"

            )

        ):

            result["aggregate"] = "MAX"

        elif any(

            word in lowered

            for word in (

                "minimum",
                "min",
                "أقل",
                "اصغر",
                "الأصغر"

            )

        ):

            result["aggregate"] = "MIN"

        return result
