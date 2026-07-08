from database.jsonb.language_detector import LanguageDetector


class JSONBResolver:

    def __init__(self):

        self.detector = LanguageDetector()

    # ---------------------------------------------------------

    def sql(self, expression):

        languages = self.detector.detect()

        parts = [

            f"{expression}->>'{lang}'"

            for lang in languages

        ]

        return (

            "COALESCE("

            +

            ", ".join(parts)

            +

            ")"

        )
