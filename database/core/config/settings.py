import os
from pathlib import Path


class Settings:

    def __init__(self):

        self.database_url = os.getenv(
            "DATABASE_URL",
            ""
        )

        self.odoo_version = os.getenv(
            "ODOO_VERSION",
            "18"
        )

        self.environment = os.getenv(
            "ENVIRONMENT",
            "development"
        )

        root = Path(__file__).resolve().parents[3]

        self.sqlite_db_path = str(
            root / "database" / "storage" / "audit.db"
        )

    def to_dict(self):

        return {
            "database_url": self.database_url,
            "odoo_version": self.odoo_version,
            "environment": self.environment,
            "sqlite_db_path": self.sqlite_db_path,
        }
