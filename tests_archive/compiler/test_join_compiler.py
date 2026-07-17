from database.compiler.join_compiler import JoinCompiler

compiler = JoinCompiler()

tests = [

    ("account_move", "res_partner"),
    ("account_move", "account_journal"),
    ("pos_order", "product_product"),

]

print()
print("=" * 80)
print("JOIN COMPILER")
print("=" * 80)

for source, target in tests:

    print()
    print(source, "->", target)

    joins = compiler.compile(source, target)

    for j in joins:
        print(j)
