from database.ai.ai_context import AIContext


ctx = AIContext()

ctx.initialize()

models = [

    "account.move",

    "res.partner",

    "product.product"

]

print()
print("=" * 70)
print("AI CONTEXT FIELDS")
print("=" * 70)

for model in models:

    print()
    print(model)
    print("-" * len(model))

    fields = sorted(ctx.fields(model))

    print(f"Total Fields : {len(fields)}")

    print()

    for field in fields:

        print(field)

    print()
