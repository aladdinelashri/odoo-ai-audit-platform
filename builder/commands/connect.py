from connectors.postgres.connection import PostgreSQLConnection


def run():

    db = PostgreSQLConnection()

    print("HOST:", db.config.host)
    print("PORT:", db.config.port)
    print("DATABASE:", db.config.database)
    print("USER:", db.config.user)
    print("PASSWORD:", repr(db.config.password))

    try:
        db.test()
        print("Database connection successful.")

    except Exception as ex:
        print(ex)