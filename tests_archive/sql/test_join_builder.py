from database.ai.ai_context import AIContext
from database.planner.execution_planner import ExecutionPlanner
from database.sql.join_builder import JoinBuilder
from database.sql.sql_builder import SQLBuilder
from database.sql.where_builder import WhereBuilder

print()
print("=" * 70)
print("JOIN BUILDER")
print("=" * 70)
print()

context = AIContext()
context.initialize()

planner = ExecutionPlanner()
where = WhereBuilder()
join = JoinBuilder(context.metadata)
builder = SQLBuilder()

queries = [

    "show invoices",

    "show invoice partner_id",

    "show invoice journal_id",

    "show invoice company_id",

    "show sale partner_id",

    "show purchase partner_id",

    "show stock product_id"

]

for query in queries:

    print(query)
    print("-" * len(query))

    plan = planner.build(query)

    plan = where.build(query, plan)

    plan = join.build(plan)

    sql = builder.build(plan)

    print(sql)

    print()
