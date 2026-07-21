"""
PostgreSQL Connection
"""

from __future__ import annotations

import os

import psycopg
from dotenv import load_dotenv


class PostgresConnection:

    def __init__(self) -> None:
        load_dotenv()

        self.connection = None

        self.config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }

    def open(self):
        self.connection = psycopg.connect(**self.config)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def fetch_all(self, query: str):
        conn = self.open()

        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            self.close()
