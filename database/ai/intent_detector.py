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

            ],

            "group": [

                "group",
                "group by",

                "حسب",
                "لكل",
                "بواسطة",
                "وفق",

                "per",
                "by"

            ],

            "top": [

                "top",
                "best",
                "highest",
                "largest",
                "ranking",

                "أفضل",
                "اعلى",
                "أعلى",
                "اكبر",
                "الأكبر",
                "ترتيب"

            ]

        }

    # ---------------------------------------------------------

    def detect(self, text):

        lowered = text.lower()

        priority = [

            "top",
            "group",
            "count",
            "sum",
            "average",
            "show"

        ]

        for intent in priority:

            for word in self.intents[intent]:

                if word.lower() in lowered:

                    return intent

        return "show"
