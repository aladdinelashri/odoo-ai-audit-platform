from database.ai.execution_planner import ExecutionPlanner
from database.response.response_formatter import ResponseFormatter
from database.sql.sql_builder import SQLBuilder
from database.sql.sql_executor import SQLExecutor

import traceback


planner = ExecutionPlanner()
builder = SQLBuilder()
executor = SQLExecutor()
formatter = ResponseFormatter()


tests = [

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


for query in tests:

    print()
    print("=" * 80)
    print(query)
    print("-" * 80)

    try:

        # ---------------------------------------------------------
        # PLAN
        # ---------------------------------------------------------

        plan = planner.build(query)

        print()
        print("PLAN")
        print(plan)

        # ---------------------------------------------------------
        # SQL
        # ---------------------------------------------------------

        sql = builder.build(plan)

        print()
        print("SQL")
        print(sql)

        # ---------------------------------------------------------
        # EXECUTE
        # ---------------------------------------------------------

        rows = executor.execute(sql)

        print()
        print("RAW RESULT TYPE")
        print(type(rows))

        print()
        print("RAW RESULT")

        if rows:

            print(rows[:5])

        else:

            print(rows)

        # ---------------------------------------------------------
        # FORMAT
        # ---------------------------------------------------------

        response = formatter.format(rows)

        print()
        print("FORMATTED RESPONSE")
        print(response)

    except Exception:

        print()
        print("FULL TRACEBACK")
        traceback.print_exc()

        break
