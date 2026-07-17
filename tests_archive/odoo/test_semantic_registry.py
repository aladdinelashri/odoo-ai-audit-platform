from database.odoo.semantic_registry import SemanticRegistry

print()
print("=" * 70)
print("SEMANTIC REGISTRY")
print("=" * 70)
print()

registry = SemanticRegistry()

registry.build()

model = "account.move"

fields = [

    "id",
    "name",
    "partner_id",
    "journal_id",
    "company_id",
    "currency_id",
    "date",
    "amount_total",
    "amount_tax",
    "amount_residual",
    "state"

]

print(model)
print()

for field in fields:

    item = registry.field(model, field)

    if not item:

        continue

    print(f"{field:20} -> {item['semantic_role']}")
