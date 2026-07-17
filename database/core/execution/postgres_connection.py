"""
PostgreSQL Connection

Architecture V40
"""

from __future__ import annotations

import os

import psycopg
from dotenv import load_dotenv


class PostgreSQLConnection:

    def __init__(self) -> None:

        load_dotenv()

        self.connection = None

        self.config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT")),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }

    def open(self):

        self.connection = psycopg.connect(**self.config)

        return self.connection

    def close(self):

        if self.connection is not None:
            self.connection.close()
            self.connection = None
