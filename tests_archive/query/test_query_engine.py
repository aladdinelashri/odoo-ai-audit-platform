from database.query.query_engine import QueryEngine


engine = QueryEngine()


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
print("QUERY ENGINE TEST")
print("=" * 80)


for query in tests:

    print()
    print("=" * 80)
    print(query)
    print("-" * 80)

    try:

        result = engine.execute(query)

        print(result)

    except Exception as ex:

        print(ex)

        break
