from database.ai.value_resolver import ValueResolver

resolver = ValueResolver()

print()
print("=" * 70)
print("VALUE RESOLVER")
print("=" * 70)
print()

tests = [

    "show posted invoices",

    "show draft invoices",

    "show paid invoices",

    "show cancelled invoices"

]

for t in tests:

    print(t)

    print(resolver.resolve(t))

    print()
