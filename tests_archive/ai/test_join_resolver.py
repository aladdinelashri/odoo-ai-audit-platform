from database.ai.entity_detector import EntityDetector
from database.ai.join_resolver import JoinResolver

resolver = JoinResolver()
detector = EntityDetector()

print()
print("=" * 70)
print("JOIN RESOLVER")
print("=" * 70)
print()

tests = [

    "show invoice partner_id",

    "show invoice journal_id",

    "show invoice company_id"

]

for text in tests:

    entities = detector.detect(text)

    model = entities["models"][0]

    joins = resolver.resolve(

        model,

        entities["fields"]

    )

    print(text)

    print()

    for j in joins:

        print(j)

    print()
