from database.ai.intent_detector import IntentDetector

print()
print("=" * 70)
print("INTENT DETECTOR")
print("=" * 70)
print()

detector = IntentDetector()

queries = [

    "show invoices",
    "list customers",
    "display products",

    "count invoices",
    "how many customers",

    "sum invoices",
    "total sales",

    "average invoice amount",

    "maximum invoice",
    "minimum invoice",

    "اعرض الفواتير",
    "عدد العملاء",
    "إجمالي الفواتير",
    "متوسط الفواتير"

]

for query in queries:

    result = detector.detect(query)

    print(f"{query:35} -> {result.name} ({result.confidence:.2f})")
