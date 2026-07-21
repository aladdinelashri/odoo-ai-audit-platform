from xmlrpc.client import ServerProxy

from database.core.odoo.xmlrpc.auth import XMLRPCAuth


class XMLRPCObjectService:
    """
    XML-RPC Object Service

    Wrapper around execute_kw.
    """

    def __init__(self):

        auth = XMLRPCAuth()

        self.url = auth.url
        self.db = auth.db
        self.username = auth.username
        self.password = auth.password
        self.uid = auth.authenticate()

        self.models = ServerProxy(
            f"{self.url}/xmlrpc/2/object",
            allow_none=True,
        )

    def execute(self, model, method, *args, **kwargs):
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
        domain=None,
        limit=None,
        offset=0,
        order=None,
    ):
        if domain is None:
            domain = []

        kwargs = {
            "offset": offset,
        }

        if limit is not None:
            kwargs["limit"] = limit

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
        domain=None,
        fields=None,
        limit=None,
        offset=0,
        order=None,
    ):
        if domain is None:
            domain = []

        kwargs = {
            "offset": offset,
        }

        if fields:
            kwargs["fields"] = fields

        if limit is not None:
            kwargs["limit"] = limit

        if order:
            kwargs["order"] = order

        return self.execute(
            model,
            "search_read",
            domain,
            **kwargs,
        )

    def search_count(
        self,
        model,
        domain=None,
    ):
        if domain is None:
            domain = []

        return self.execute(
            model,
            "search_count",
            domain,
        )

    def create(
        self,
        model,
        values,
    ):
        return self.execute(
            model,
            "create",
            values,
        )

    def write(
        self,
        model,
        ids,
        values,
    ):
        return self.execute(
            model,
            "write",
            ids,
            values,
        )

    def unlink(
        self,
        model,
        ids,
    ):
        return self.execute(
            model,
            "unlink",
            ids,
        )
