from database.ai.engine import AIEngine

engine = AIEngine()

questions = [

    "show invoices",

    "show customers",

    "show products",

]

print()
print("=" * 80)
print("SQL BUILDER")
print("=" * 80)

for q in questions:

    print()
    print(q)
    print("-" * 80)

    sql = engine.build_sql(q)

    print(sql)
