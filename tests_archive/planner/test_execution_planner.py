from database.planner.execution_planner import ExecutionPlanner

print()
print("=" * 70)
print("EXECUTION PLANNER")
print("=" * 70)
print()

planner = ExecutionPlanner()

queries = [

    "show invoices",

    "show customers",

    "show products",

    "count invoices",

    "sum invoices",

    "average invoice amount",

    "show invoice amount_total",

    "show customer email",

    "show product list_price"

]

for query in queries:

    print(query)
    print("-" * len(query))

    plan = planner.build(query)

    print(plan)

    print()
