from database.schema.schema_extractor import SchemaExtractor

extractor = SchemaExtractor()

print()
print("=" * 70)
print("SCHEMA EXTRACTOR")
print("=" * 70)
print()

tables = extractor.tables()

print("Tables :", len(tables))
print()

columns = extractor.columns("account_move")

print("Columns :", len(columns))
print()

relations = extractor.foreign_keys("account_move")

print("Foreign Keys :", len(relations))
print()

for relation in relations:

    print(relation)
