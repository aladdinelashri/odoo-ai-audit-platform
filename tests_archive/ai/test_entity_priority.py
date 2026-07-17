from database.ai.entity_detector import EntityDetector

print()
print("=" * 70)
print("PRIMARY ENTITY DETECTOR")
print("=" * 70)
print()

detector = EntityDetector()

queries = [

    "show invoice journal_id",

    "show invoice partner_id",

    "show invoice company_id",

    "show sale partner_id",

    "show purchase partner_id",

    "show stock product_id",

    "show pos partner_id",

    "show invoice amount_total",

]

for query in queries:

    print(query)
    print("-" * len(query))

    result = detector.detect(query)

    print(result)

    print()
