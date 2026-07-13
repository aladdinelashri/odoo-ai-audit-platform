import re


class WhereBuilder:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def build(self, text, plan):

        filters = []

        lowered = text.lower()

        # -------------------------------------------------
        # state
        # -------------------------------------------------

        states = [

            "draft",
            "posted",
            "cancel",
            "paid",
            "done",
            "sale",
            "purchase"

        ]

        for state in states:

            if state in lowered:

                filters.append(

                    f"state = '{state}'"

                )

        # -------------------------------------------------
        # amount >
        # -------------------------------------------------

        match = re.search(

            r"(greater than|more than|above)\s+([0-9]+)",

            lowered

        )

        if match:

            value = match.group(2)

            filters.append(

                f"amount_total > {value}"

            )

        # -------------------------------------------------
        # amount <
        # -------------------------------------------------

        match = re.search(

            r"(less than|below|under)\s+([0-9]+)",

            lowered

        )

        if match:

            value = match.group(2)

            filters.append(

                f"amount_total < {value}"

            )

        # -------------------------------------------------
        # date =
        # -------------------------------------------------

        match = re.search(

            r"([0-9]{4}-[0-9]{2}-[0-9]{2})",

            lowered

        )

        if match:

            filters.append(

                f"date = '{match.group(1)}'"

            )

        plan["filters"] = filters

        return plan
