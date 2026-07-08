import re


class ParameterDetector:

    def detect(self, text):

        result = {

            "limit": None,

            "order": "DESC"

        }

        m = re.search(

            r"(?:last|آخر)\s+(\d+)",

            text,

            re.IGNORECASE

        )

        if m:

            result["limit"] = int(m.group(1))

            result["order"] = "DESC"

            return result

        m = re.search(

            r"(?:first|أول)\s+(\d+)",

            text,

            re.IGNORECASE

        )

        if m:

            result["limit"] = int(m.group(1))

            result["order"] = "ASC"

            return result

        return result
