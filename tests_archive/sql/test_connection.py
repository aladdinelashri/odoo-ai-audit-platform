from database.sql.connection import DatabaseConnection


print()
print("=" * 70)
print("DATABASE CONNECTION")
print("=" * 70)
print()

db = DatabaseConnection()

try:

    connection = db.open()

    cursor = connection.cursor()

    cursor.execute("SELECT version();")

    row = cursor.fetchone()

    print("Connected Successfully")
    print()
    print(row["version"])

finally:

    db.close()

print()
