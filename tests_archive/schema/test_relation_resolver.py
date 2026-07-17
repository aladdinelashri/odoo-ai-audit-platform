from database.resolver.relation_resolver import RelationResolver

resolver = RelationResolver()

tests = [

    ("account_move", "res_partner"),
    ("account_move", "account_journal"),
    ("pos_order", "res_partner"),
    ("pos_order", "product_product")

]

print()
print("=" * 80)
print("RELATION RESOLVER")
print("=" * 80)

for source, target in tests:

    print()
    print(source, "->", target)

    print(

        resolver.resolve(

            source,

            target

        )

    )
