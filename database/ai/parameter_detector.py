import re


class ParameterDetector:

    def __init__(self):

        self.desc_words = [

            "last",
            "latest",
            "recent",
            "آخر",
            "اخر"

        ]

        self.asc_words = [

            "first",
            "oldest",
            "أول",
            "اول"

        ]

    # ---------------------------------------------------------

    def detect(self, text):

        text = text.lower()

        result = {

            "limit": None,

            "order": None

        }

        # ------------------------------------------
        # limit
        # ------------------------------------------

        m = re.search(r"\b(\d+)\b", text)

        if m:

            result["limit"] = int(

                m.group(1)

            )

        # ------------------------------------------
        # order
        # ------------------------------------------

        for word in self.desc_words:

            if word in text:

                result["order"] = "DESC"

                break

        if result["order"] is None:

            for word in self.asc_words:

                if word in text:

                    result["order"] = "ASC"

                    break

        return result
