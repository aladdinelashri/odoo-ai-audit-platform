from database.ai.entity_detector import EntityDetector

print()
print("=" * 70)
print("ENTITY DETECTOR")
print("=" * 70)
print()

detector = EntityDetector()

queries = [

    "show invoices",
    "show customers",
    "show products",
    "show sales orders",
    "show purchase orders",
    "show stock moves",
    "show pos orders",
    "show invoice amount_total",
    "show customer email",
    "show product list_price"

]

for query in queries:

    print(query)
    print("-" * len(query))

    result = detector.detect(query)

    print(result)
    print()
