from database.odoo.knowledge_catalog import KnowledgeCatalog

print()
print("=" * 70)
print("KNOWLEDGE CATALOG")
print("=" * 70)
print()

catalog = KnowledgeCatalog()

catalog.build()

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

    item = catalog.model(model)

    print(model)

    if not item:

        print("Not Found")
        print()
        continue

    print("Table      :", item["table"])
    print("Fields     :", len(item["fields"]))
    print("Relations  :", len(item["relations"]))

    print()
