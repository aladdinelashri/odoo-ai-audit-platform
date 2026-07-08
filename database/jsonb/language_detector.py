from database.sql.executor import SQLExecutor


class LanguageDetector:

    def __init__(self):

        self.db = SQLExecutor()

        self.languages = None

    # ---------------------------------------------------------

    def detect(self):

        if self.languages is not None:

            return self.languages

        sql = """

        SELECT name

        FROM account_journal

        WHERE name IS NOT NULL

        LIMIT 50

        """

        rows = self.db.execute(sql)

        langs = set()

        for row in rows:

            value = row["name"]

            if isinstance(value, dict):

                langs.update(value.keys())

        if not langs:

            langs = {"en_US"}

        self.languages = sorted(langs)

        return self.languages
