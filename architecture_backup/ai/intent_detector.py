from dataclasses import dataclass
import re


@dataclass
class Intent:

    name: str

    confidence: float


class IntentDetector:

    def __init__(self):

        self.rules = [

            (
                "count",
                [
                    "count",
                    "how many",
                    "number of",
                    "عدد",
                    "كم عدد"
                ]
            ),

            (
                "sum",
                [
                    "sum",
                    "total",
                    "total amount",
                    "اجمالي",
                    "إجمالي",
                    "مجموع"
                ]
            ),

            (
                "average",
                [
                    "average",
                    "avg",
                    "mean",
                    "متوسط"
                ]
            ),

            (
                "max",
                [
                    "maximum",
                    "max",
                    "highest",
                    "largest",
                    "اكبر",
                    "أكبر",
                    "اعلى",
                    "أعلى"
                ]
            ),

            (
                "min",
                [
                    "minimum",
                    "min",
                    "smallest",
                    "اقل",
                    "أقل"
                ]
            ),

            (
                "list",
                [
                    "show",
                    "list",
                    "display",
                    "get",
                    "اعرض",
                    "عرض",
                    "اظهر",
                    "أظهر",
                    "هات"
                ]
            )

        ]

    # ---------------------------------------------------------

    def detect(self, text):

        lowered = text.lower()

        for intent, keywords in self.rules:

            for keyword in keywords:

                if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", lowered):

                    return Intent(

                        name=intent,

                        confidence=1.0

                    )

        return Intent(

            name="list",

            confidence=0.50

        )
