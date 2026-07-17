from database.sql.sql_executor import SQLExecutor


print()
print("=" * 70)
print("SQL EXECUTOR")
print("=" * 70)
print()

executor = SQLExecutor()

try:

    sql = """
    SELECT
        name,
        amount_total,
        state
    FROM account_move
    ORDER BY id DESC
    LIMIT 5
    """

    rows = executor.execute(sql)

    print(f"Rows Returned : {len(rows)}")
    print()

    for row in rows:

        print(row)

finally:

    executor.close()

print()
