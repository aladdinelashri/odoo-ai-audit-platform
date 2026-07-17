import psycopg2
from psycopg2.extras import RealDictCursor

from database.config.settings import settings


class DatabaseConnection:

    def __init__(self):

        self.connection = None

    # ---------------------------------------------------------

    def open(self):

        if self.connection:

            return self.connection

        self.connection = psycopg2.connect(

            host=settings.database.host,
            port=settings.database.port,
            dbname=settings.database.database,
            user=settings.database.user,
            password=settings.database.password,
            cursor_factory=RealDictCursor

        )

        self.connection.autocommit = True

        return self.connection

    # ---------------------------------------------------------

    def cursor(self):

        return self.open().cursor()

    # ---------------------------------------------------------

    def close(self):

        if self.connection:

            self.connection.close()

            self.connection = None
