from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, URL

from connectors.postgres.config import get_database_config


class PostgreSQLConnection:

    def __init__(self):
        self.config = get_database_config()
        self.engine: Engine | None = None

    def connect(self) -> Engine:

        if self.engine is None:

            url = URL.create(
                drivername="postgresql+psycopg",
                username=self.config.user,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
            )

            self.engine = create_engine(
                url,
                pool_pre_ping=True,
                pool_recycle=3600,
                future=True,
            )

        return self.engine

    def test(self) -> bool:

        engine = self.connect()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return True