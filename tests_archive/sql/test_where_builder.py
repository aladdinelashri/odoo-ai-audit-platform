from database.planner.execution_planner import ExecutionPlanner
from database.sql.where_builder import WhereBuilder
from database.sql.sql_builder import SQLBuilder

print()
print("=" * 70)
print("WHERE BUILDER")
print("=" * 70)
print()

planner = ExecutionPlanner()
where = WhereBuilder()
sql = SQLBuilder()

queries = [

    "show posted invoices",

    "show draft invoices",

    "show invoices greater than 1000",

    "show invoices less than 500",

    "show invoices 2025-01-01",

    "show posted invoices greater than 1000"

]

for query in queries:

    print(query)
    print("-" * len(query))

    plan = planner.build(query)

    plan = where.build(

        query,

        plan

    )

    statement = sql.build(plan)

    print(statement)

    print()
