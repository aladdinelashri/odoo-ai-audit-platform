from database.ai.query_engine import QueryEngine
from database.sql.executor import SQLExecutor


class QueryExecutor:

    def __init__(self):

        self.engine = QueryEngine()

        self.db = SQLExecutor()

    # ---------------------------------------------------------

    def execute(self, text):

        info = self.engine.build_sql(text)

        rows = self.db.execute(

            info["sql"]

        )

        return {

            "query": text,

            "parsed": info["parsed"],

            "plan": info["plan"],

            "sql": info["sql"],

            "rows": rows

        }
