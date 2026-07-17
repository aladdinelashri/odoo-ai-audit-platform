from database.odoo.database_field_resolver import DatabaseFieldResolver


resolver = DatabaseFieldResolver()

print()
print("=" * 70)
print("DATABASE FIELD RESOLVER")
print("=" * 70)
print()

tests = [

    ("account.move", "display_name"),

    ("account.move", "amount_total"),

    ("res.partner", "display_name"),

    ("product.product", "display_name"),

]

for model, field in tests:

    print(field, " -> ", resolver.resolve(model, field))
