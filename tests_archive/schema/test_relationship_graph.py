from database.schema.relationship_graph import RelationshipGraph


graph = RelationshipGraph()

print()

print("=" * 80)
print("RELATIONSHIP GRAPH")
print("=" * 80)

print()

print("Tables    :", len(graph.tables()))
print("Relations :", graph.relation_count())

assert len(graph.tables()) > 0
assert graph.relation_count() > 0

print()
print("OK")
