import os


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


    def to_dict(self):

        return {
            "database_url": self.database_url,
            "odoo_version": self.odoo_version,
            "environment": self.environment
        }
