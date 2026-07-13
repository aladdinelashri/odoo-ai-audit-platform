from database.schema.relationship_graph import RelationshipGraph
from database.schema.path_finder import PathFinder


graph = RelationshipGraph()

finder = PathFinder(graph)

print()

print("=" * 80)
print("PATH FINDER")
print("=" * 80)

pairs = [

    ("account_move", "res_partner"),
    ("account_move", "account_journal"),
    ("pos_order", "res_partner"),
    ("pos_order", "product_product")

]

for source, target in pairs:

    print()

    print(source, "->", target)

    path = finder.find(source, target)

    print(path)
