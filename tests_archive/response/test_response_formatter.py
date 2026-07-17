from database.response.response_formatter import ResponseFormatter


formatter = ResponseFormatter()

print("=" * 70)
print("LIST")
print("=" * 70)

rows = [
    {"name": "INV001", "amount": 100},
    {"name": "INV002", "amount": 200}
]

print(formatter.format(rows))


print()

print("=" * 70)
print("AGGREGATE")
print("=" * 70)

rows = [
    {"count": 250}
]

print(formatter.format(rows))


print()

print("=" * 70)
print("EMPTY")
print("=" * 70)

print(formatter.format([]))


print()

print("=" * 70)
print("ERROR")
print("=" * 70)

print(

    formatter.format(

        Exception("Database Error")

    )

)
