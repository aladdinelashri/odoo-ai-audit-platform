import re
from datetime import date, timedelta


class DateResolver:

    # ---------------------------------------------------------

    def resolve(self, text):

        lowered = text.lower()

        today = date.today()

        filters = []

        # ------------------------------------------
        # Explicit Date (YYYY-MM-DD)
        # ------------------------------------------

        matches = re.findall(

            r"\d{4}-\d{2}-\d{2}",

            lowered

        )

        if matches:

            filters.append(

                {

                    "field": "date",

                    "operator": "=",

                    "value": matches[0]

                }

            )

            return filters

        # ------------------------------------------
        # Today
        # ------------------------------------------

        if "today" in lowered:

            filters.append(

                {

                    "field": "date",

                    "operator": "=",

                    "value": today.isoformat()

                }

            )

            return filters

        # ------------------------------------------
        # Yesterday
        # ------------------------------------------

        if "yesterday" in lowered:

            filters.append(

                {

                    "field": "date",

                    "operator": "=",

                    "value": (

                        today - timedelta(days=1)

                    ).isoformat()

                }

            )

            return filters

        # ------------------------------------------
        # This Month
        # ------------------------------------------

        if "this month" in lowered:

            start = today.replace(day=1)

            filters.append(

                {

                    "field": "date",

                    "operator": ">=",

                    "value": start.isoformat()

                }

            )

            return filters

        # ------------------------------------------
        # This Year
        # ------------------------------------------

        if "this year" in lowered:

            start = today.replace(

                month=1,

                day=1

            )

            filters.append(

                {

                    "field": "date",

                    "operator": ">=",

                    "value": start.isoformat()

                }

            )

            return filters

        return filters
