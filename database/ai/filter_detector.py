class FilterDetector:

    def __init__(self):

        self.operators = {

            ">": [

                "greater than",
                "more than",
                "over",
                "above",

                "أكبر من",
                "أكثر من",
                "يزيد عن",
                "فوق"

            ],

            "<": [

                "less than",
                "below",
                "under",

                "أقل من",
                "أصغر من",
                "تحت"

            ],

            "=": [

                "equals",
                "equal",

                "يساوي",
                "بـ"

            ]

        }

    # ---------------------------------------------------------

    def detect(self, text):

        return []
