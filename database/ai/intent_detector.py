import re


class IntentDetector:

    def __init__(self):

        self.intents = {

            "show": [

                "show",
                "list",
                "display",
                "find",
                "get",
                "اعرض",
                "اظهر",
                "هات",
                "اعطني",
                "اعطنى",
                "عرض"

            ],

            "count": [

                "count",
                "how many",
                "عدد",
                "كم",
                "احصاء"

            ],

            "sum": [

                "sum",
                "total",
                "اجمالي",
                "إجمالي",
                "مجموع"

            ],

            "average": [

                "average",
                "avg",
                "متوسط"

            ]

        }

    # ---------------------------------------------------------

    def detect(self, text):

        text = text.lower()

        for intent, words in self.intents.items():

            for word in words:

                if re.search(r"\b" + re.escape(word.lower()) + r"\b", text):

                    return intent

        return "show"
