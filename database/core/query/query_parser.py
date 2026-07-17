class QueryParser:

    def parse(self, text: str):
        text = text.strip()

        return {
            "raw": text,
            "tokens": text.split()
        }
