from database.odoo.business_dictionary_builder import BusinessDictionaryBuilder

print()
print("=" * 70)
print("BUSINESS DICTIONARY BUILDER")
print("=" * 70)
print()

builder = BusinessDictionaryBuilder()

dictionary = builder.build()

print("Models :", len(dictionary))
print()

tests = [

    "account.move",
    "res.partner",
    "product.product",
    "product.template",
    "sale.order",
    "purchase.order",
    "stock.move",
    "pos.order"

]

for model in tests:

    aliases = dictionary.get(model, [])

    print(model)
    print("-" * len(model))

    for alias in aliases:

        print(" ", alias)

    print()
