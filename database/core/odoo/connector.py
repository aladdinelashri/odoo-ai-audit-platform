"""
Odoo XML-RPC Connector — Production-ready for SaaS multi-tenant.
"""
import xmlrpc.client
from typing import List, Dict, Any, Optional

from config.settings import Settings


class OdooConnector:
    """Connects to Odoo via XML-RPC and provides search_read interface."""

    def __init__(self, url: str = None, db: str = None,
                 username: str = None, password: str = None):
        self.url = url or Settings.ODOO_URL
        self.db = db or Settings.ODOO_DB
        self.username = username or Settings.ODOO_USERNAME
        self.password = password or Settings.ODOO_PASSWORD

        self.uid: Optional[int] = None
        self._common = None
        self._object = None
        self._connect()

    def _connect(self):
        """Authenticate and store proxies."""
        self._common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self._object = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self.uid = self._common.authenticate(
            self.db, self.username, self.password, {}
        )
        if not self.uid:
            raise ConnectionError(
                f"Odoo authentication failed for {self.username}@{self.db}"
            )

    def search_read(self, model: str, domain: list, fields: list,
                    limit: int = 0, offset: int = 0, order: str = None) -> List[Dict]:
        """Odoo search_read wrapper."""
        kwargs = {"fields": fields, "limit": limit, "offset": offset}
        if order:
            kwargs["order"] = order
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "search_read", [domain], kwargs
        )

    def search(self, model: str, domain: list, limit: int = 0) -> List[int]:
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "search", [domain], {"limit": limit}
        )

    def read(self, model: str, ids: list, fields: list) -> List[Dict]:
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "read", [ids], {"fields": fields}
        )

    def create(self, model: str, values: dict) -> int:
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "create", [values]
        )

    def write(self, model: str, ids: list, values: dict) -> bool:
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "write", [ids, values]
        )

    def __repr__(self):
        return f"<OdooConnector {self.username}@{self.db} uid={self.uid}>"
