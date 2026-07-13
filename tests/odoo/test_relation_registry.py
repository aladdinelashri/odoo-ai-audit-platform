from database.odoo.relation_registry import RelationRegistry

print()
print("=" * 70)
print("RELATION REGISTRY")
print("=" * 70)
print()

registry = RelationRegistry()

registry.build()

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

    print(model)

    relations = registry.relations(model)

    print("Relations :", len(relations))

    for item in relations[:10]:

        print(
            f"  {item['source_field']}  -->  "
            f"{item['target_model']} ({item['target_table']})"
        )

    print()
