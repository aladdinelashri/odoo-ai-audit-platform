from database.ai.engine import AIEngine


engine = AIEngine()

queries = [

    "show invoices",

    "show customers",

    "show products",

    "show sales orders",

    "count invoices",

    "sum invoices",

    "average invoice amount"

]

print("\n" + "=" * 80)
print("AI ENGINE INTEGRATION TEST")
print("=" * 80)

for query in queries:

    print(f"\nQuery : {query}")
    print("-" * 80)

    sql = engine.build_sql(query)

    print(sql)
