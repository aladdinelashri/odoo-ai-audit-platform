class JSONBResolver:

    def __init__(self, language="ar_001"):

        self.language = language

    def text(self, value):

        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if not isinstance(value, dict):
            return str(value)

        if self.language in value:
            return value[self.language]

        if "en_US" in value:
            return value["en_US"]

        if "1" in value:
            return value["1"]

        for v in value.values():
            if v:
                return v

        return ""

    def account_code(self, value):

        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if not isinstance(value, dict):
            return str(value)

        return value.get("1", "")
