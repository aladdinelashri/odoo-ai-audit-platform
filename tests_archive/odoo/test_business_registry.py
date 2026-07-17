from database.odoo.business_registry import BusinessRegistry

registry = BusinessRegistry().aliases()

print("=" * 80)
print("BUSINESS REGISTRY")
print("=" * 80)

tests = [

    "Account",
    "Analytic Account",
    "Access Management",
    "الحساب",
    "الحساب التحليلي"

]

for item in tests:

    print(item)

    print(registry.get(item.lower()))

    print()
