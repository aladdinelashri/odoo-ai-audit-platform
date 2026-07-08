from database.planner.field_optimizer import FieldOptimizer
from database.planner.join_optimizer import JoinOptimizer
from database.planner.query_optimizer import QueryOptimizer


class Planner:

    def __init__(self):

        self.fields = FieldOptimizer()

        self.joins = JoinOptimizer()

        self.optimizer = QueryOptimizer()

    # ---------------------------------------------------------

    def build(self, report):

        table = report["table"]

        fields = self.fields.optimize(

            table,

            report.get("fields", [])

        )

        joins = self.joins.optimize(

            table,

            report.get("fields", [])

        )

        plan = {

            "table": table,

            "select": fields,

            "joins": joins,

            "where": report.get("filters", []),

            "order": report.get("order_by", [])

        }

        return self.optimizer.optimize(plan)
