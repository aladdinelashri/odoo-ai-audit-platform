import re
from datetime import date, timedelta

from database.ai.value_resolver import ValueResolver


class ParameterResolver:

    def __init__(self):

        self.values = ValueResolver()

    # ---------------------------------------------------------

    def resolve(self, text):

        lowered = text.lower()

        today = date.today()

        result = {

            "filters": [],

            "limit": None,

            "order": None

        }

        # -------------------------------------------------
        # Semantic Values
        # -------------------------------------------------

        result["filters"].extend(

            self.values.resolve(lowered)

        )

        # -------------------------------------------------
        # Date
        # -------------------------------------------------

        matches = re.findall(

            r"\d{4}-\d{2}-\d{2}",

            lowered

        )

        if matches:

            result["filters"].append(

                {

                    "field": "date",

                    "operator": "=",

                    "value": matches[0]

                }

            )

        elif "today" in lowered:

            result["filters"].append(

                {

                    "field": "date",

                    "operator": "=",

                    "value": today.isoformat()

                }

            )

        elif "yesterday" in lowered:

            result["filters"].append(

                {

                    "field": "date",

                    "operator": "=",

                    "value": (

                        today - timedelta(days=1)

                    ).isoformat()

                }

            )

        elif "this month" in lowered:

            result["filters"].append(

                {

                    "field": "date",

                    "operator": ">=",

                    "value": today.replace(day=1).isoformat()

                }

            )

        elif "this year" in lowered:

            result["filters"].append(

                {

                    "field": "date",

                    "operator": ">=",

                    "value": today.replace(

                        month=1,

                        day=1

                    ).isoformat()

                }

            )

        # -------------------------------------------------
        # Numeric Comparison
        # -------------------------------------------------

        comparisons = [

            ("greater than", ">"),

            ("less than", "<"),

            ("more than", ">"),

            ("under", "<"),

            ("over", ">"),

            ("=", "=")

        ]

        for phrase, operator in comparisons:

            pattern = rf"{phrase}\s+(\d+(?:\.\d+)?)"

            match = re.search(

                pattern,

                lowered

            )

            if match:

                result["filters"].append(

                    {

                        "field": None,

                        "operator": operator,

                        "value": float(

                            match.group(1)

                        )

                    }

                )

                break

        # -------------------------------------------------
        # Limit
        # -------------------------------------------------

        match = re.search(

            r"(top|first)\s+(\d+)",

            lowered

        )

        if match:

            result["limit"] = int(

                match.group(2)

            )

        # -------------------------------------------------
        # Order
        # -------------------------------------------------

        if "latest" in lowered:

            result["order"] = "DESC"

        elif "oldest" in lowered:

            result["order"] = "ASC"

        return result
