from database.validator.sql_validator import SQLValidator


validator = SQLValidator()

validator.allow_tables(

    [

        "account_move",

        "account_move_line",

        "res_partner"

    ]

)


print("=" * 70)
print("VALID SQL")
print("=" * 70)

sql = """

SELECT id,name

FROM account_move

WHERE amount_total > 1000

"""

try:

    print(

        validator.validate(sql)

    )

except Exception as ex:

    print(ex)


print()

print("=" * 70)
print("INSERT")
print("=" * 70)

sql = """

INSERT INTO account_move

VALUES (1)

"""

try:

    print(

        validator.validate(sql)

    )

except Exception as ex:

    print(ex)


print()

print("=" * 70)
print("DELETE")
print("=" * 70)

sql = """

DELETE FROM account_move

"""

try:

    print(

        validator.validate(sql)

    )

except Exception as ex:

    print(ex)


print()

print("=" * 70)
print("DROP")
print("=" * 70)

sql = """

DROP TABLE account_move

"""

try:

    print(

        validator.validate(sql)

    )

except Exception as ex:

    print(ex)


print()

print("=" * 70)
print("UNKNOWN TABLE")
print("=" * 70)

sql = """

SELECT *

FROM users

"""

try:

    print(

        validator.validate(sql)

    )

except Exception as ex:

    print(ex)


print()

print("=" * 70)
print("MULTIPLE STATEMENTS")
print("=" * 70)

sql = """

SELECT *

FROM account_move;

DELETE FROM account_move

"""

try:

    print(

        validator.validate(sql)

    )

except Exception as ex:

    print(ex)
