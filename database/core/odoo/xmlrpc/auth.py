import os
import xmlrpc.client
from pathlib import Path

from dotenv import dotenv_values


PROJECT_ROOT = Path(__file__).resolve().parents[4]
ENV_FILE = PROJECT_ROOT / ".env"

CONFIG = dotenv_values(ENV_FILE)


class XMLRPCAuth:
    def __init__(self):
        self.url = CONFIG["ODOO_URL"]
        self.db = CONFIG["ODOO_DB"]
        self.username = CONFIG["ODOO_USERNAME"]
        self.password = CONFIG["ODOO_PASSWORD"]

    def authenticate(self):
        common = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/common",
            allow_none=True,
        )

        return common.authenticate(
            self.db,
            self.username,
            self.password,
            {},
        )

    def version(self):
        common = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/common",
            allow_none=True,
        )

        return common.version()
