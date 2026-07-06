from database.sql.executor import SQLExecutor
from database.sql.query_builder import QueryBuilder


def run():

    print()
    print("=== SQL Audit ===")
    print()

    executor = SQLExecutor()
    queries = QueryBuilder()

    summary = executor.execute(
        queries.account_move_summary()
    )

    print("Account Move Summary")
    print(summary)

    print()

    duplicates = executor.execute(
        queries.duplicate_payment_reference()
    )

    print("Duplicate Payment References")
    print(f"Found: {len(duplicates)}")

    print()

    large_entries = executor.execute(
        queries.large_entries(),
        {"limit": 100000}
    )

    print("Large Journal Entries")
    print(f"Found: {len(large_entries)}")
    print()

    for row in large_entries[:10]:

        print(
            f"{row['id']} | "
            f"{row['date']} | "
            f"{row['name']} | "
            f"{row['amount_total']}"
        )

    print()
    print("===================================")
    print(" SQL Audit Completed")
    print("===================================")
