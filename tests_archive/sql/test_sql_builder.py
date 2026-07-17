from database.planner.execution_planner import ExecutionPlanner
from database.sql.sql_builder import SQLBuilder

print()
print("=" * 70)
print("SQL BUILDER")
print("=" * 70)
print()

planner = ExecutionPlanner()
builder = SQLBuilder()

queries = [

    "show invoices",

    "count invoices",

    "sum invoices",

    "average invoice amount",

    "show customers",

    "show products",

    "show invoice amount_total"

]

for query in queries:

    print(query)
    print("-" * len(query))

    plan = planner.build(query)

    sql = builder.build(plan)

    print(sql)

    print()
