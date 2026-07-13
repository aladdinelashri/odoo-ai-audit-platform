class ValueResolver:

    def __init__(self):

        self.VALUES = {

            "posted": {

                "field": "state",

                "value": "posted"

            },

            "draft": {

                "field": "state",

                "value": "draft"

            },

            "cancelled": {

                "field": "state",

                "value": "cancel"

            },

            "cancel": {

                "field": "state",

                "value": "cancel"

            },

            "paid": {

                "field": "payment_state",

                "value": "paid"

            }

        }

    # ---------------------------------------------------------

    def resolve(self, text):

        lowered = text.lower()

        filters = []

        seen = set()

        aliases = sorted(

            self.VALUES.items(),

            key=lambda x: len(x[0]),

            reverse=True

        )

        for keyword, info in aliases:

            if keyword in lowered:

                key = (

                    info["field"],

                    info["value"]

                )

                if key not in seen:

                    seen.add(key)

                    filters.append({

                        "field": info["field"],

                        "operator": "=",

                        "value": info["value"]

                    })

                lowered = lowered.replace(keyword, " ")

        return filters
