from database.planner.execution_planner import ExecutionPlanner
from database.sql.sql_builder import SQLBuilder
from database.sql.sql_executor import SQLExecutor


planner = ExecutionPlanner()
builder = SQLBuilder()
executor = SQLExecutor()


queries = [

    "show invoices",

    "show posted invoices",

    "show posted invoices greater than 1000",

    "show invoices less than 500",

    "count invoices",

    "sum invoices",

    "average invoice amount"

]


print()
print("=" * 80)
print("END TO END TEST")
print("=" * 80)
print()


for question in queries:

    print()
    print("=" * 80)
    print(question)
    print("-" * 80)

    try:

        plan = planner.build(question)

        print()

        print("PLAN")

        print(plan)

        print()

        sql = builder.build(plan)

        print("SQL")

        print(sql)

        print()

        rows = executor.execute(sql)

        print("ROWS :", len(rows))

        print()

        for row in rows[:5]:

            print(row)

    except Exception as ex:

        print("ERROR")

        print(ex)

print()

executor.close()
