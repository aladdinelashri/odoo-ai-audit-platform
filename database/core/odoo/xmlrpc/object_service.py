import xmlrpc.client

from database.core.odoo.xmlrpc.auth import XMLRPCAuth


class XMLRPCObjectService:
    """
    Generic XML-RPC Object Service.

    Provides reusable wrappers around Odoo's execute_kw API.
    """

    def __init__(self):
        self.auth = XMLRPCAuth()

        self.url = self.auth.url
        self.db = self.auth.db
        self.username = self.auth.username
        self.password = self.auth.password

        self.uid = self.auth.authenticate()

        if not self.uid:
            raise RuntimeError("XML-RPC authentication failed.")

        self.models = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/object",
            allow_none=True,
        )

    def execute(self, model, method, *args, **kwargs):
        """
        Generic execute_kw wrapper.
        """
        return self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            method,
            list(args),
            kwargs,
        )

    def search(
        self,
        model,
        domain,
        limit=None,
        offset=0,
        order=None,
    ):
        kwargs = {}

        if limit is not None:
            kwargs["limit"] = limit

        if offset:
            kwargs["offset"] = offset

        if order:
            kwargs["order"] = order

        return self.execute(
            model,
            "search",
            domain,
            **kwargs,
        )

    def read(
        self,
        model,
        ids,
        fields=None,
    ):
        kwargs = {}

        if fields:
            kwargs["fields"] = fields

        return self.execute(
            model,
            "read",
            ids,
            **kwargs,
        )

    def search_read(
        self,
        model,
        domain,
        fields=None,
        limit=None,
        offset=0,
        order=None,
    ):
        kwargs = {}

        if fields:
            kwargs["fields"] = fields

        if limit is not None:
            kwargs["limit"] = limit

        if offset:
            kwargs["offset"] = offset

        if order:
            kwargs["order"] = order

        return self.execute(
            model,
            "search_read",
            domain,
            **kwargs,
        )

    def fields_get(self, model):
        """
        Retrieve model field definitions.
        """
        return self.execute(
            model,
            "fields_get",
        )
