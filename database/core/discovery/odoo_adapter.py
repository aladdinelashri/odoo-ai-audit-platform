"""
Odoo Client Adapter — Wraps any Odoo connector to provide search_read().
Works with xmlrpc.client, odoorpc, erppeek, or custom connectors.
"""
import xmlrpc.client


class OdooClientAdapter:
    """Universal adapter for Odoo XML-RPC connections."""

    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self._common = None
        self._object = None
        self._authenticate()

    def _authenticate(self):
        self._common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self._object = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self.uid = self._common.authenticate(self.db, self.username, self.password, {})

    def search_read(self, model, domain, fields, limit=0, offset=0, order=None):
        kwargs = {"fields": fields, "limit": limit, "offset": offset}
        if order:
            kwargs["order"] = order
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "search_read", [domain], kwargs
        )

    def search(self, model, domain, limit=0):
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "search", [domain], {"limit": limit}
        )

    def read(self, model, ids, fields):
        return self._object.execute_kw(
            self.db, self.uid, self.password,
            model, "read", [ids], {"fields": fields}
        )
