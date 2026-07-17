from database.odoo.metadata_service import MetadataService

print()
print("=" * 70)
print("METADATA SERVICE")
print("=" * 70)
print()

service = MetadataService()

models = [

    "account.move",
    "res.partner",
    "product.template",
    "sale.order",
    "purchase.order",
    "stock.move",
    "pos.order"

]

for model in models:

    info = service.model_info(model)

    print(model)
    print("-" * len(model))

    print("Table :", info["table"])
    print("Fields :", len(info["fields"]))
    print("Relations :", len(info["relations"]))
    print("Default :", service.default_fields(model)[:6])

    print()
