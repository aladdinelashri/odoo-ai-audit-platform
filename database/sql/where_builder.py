import re


class WhereBuilder:

    def build(self, text, plan):

        filters = []

        lowered = text.lower()

        states = [
            "draft",
            "posted",
            "cancel",
            "paid",
            "done",
            "sale",
            "purchase",
        ]

        for state in states:

            if state in lowered:

                filters.append(
                    {
                        "field": "state",
                        "operator": "=",
                        "value": state,
                    }
                )

        match = re.search(
            r"(greater than|more than|above)\s+([0-9]+)",
            lowered,
        )

        if match:

            filters.append(
                {
                    "field": "amount_total",
                    "operator": ">",
                    "value": int(match.group(2)),
                }
            )

        match = re.search(
            r"(less than|below|under)\s+([0-9]+)",
            lowered,
        )

        if match:

            filters.append(
                {
                    "field": "amount_total",
                    "operator": "<",
                    "value": int(match.group(2)),
                }
            )

        match = re.search(
            r"([0-9]{4}-[0-9]{2}-[0-9]{2})",
            lowered,
        )

        if match:

            filters.append(
                {
                    "field": "date",
                    "operator": "=",
                    "value": match.group(1),
                }
            )

        plan["filters"] = filters

        return plan
