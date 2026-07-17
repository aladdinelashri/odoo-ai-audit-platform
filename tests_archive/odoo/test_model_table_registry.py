from database.odoo.model_table_registry import ModelTableRegistry

print()
print("=" * 70)
print("MODEL ↔ TABLE REGISTRY")
print("=" * 70)
print()

registry = ModelTableRegistry()

data = registry.build()

print("Models :", len(data))
print()

tests = [

    "account.move",
    "account.payment",
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

    print(" -> ", registry.table(model))

    print()
