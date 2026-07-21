from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


class UserReader:
    """
    Reader for res.users

    Read-only access layer.
    """

    MODEL = "res.users"

    def __init__(self):
        self.service = XMLRPCObjectService()

    def first(self):
        users = self.service.search_read(
            self.MODEL,
            [],
            fields=["id", "name", "login"],
            limit=1,
        )
        return users[0] if users else None

    def by_id(self, user_id):
        users = self.service.read(
            self.MODEL,
            [user_id],
            fields=["id", "name", "login"],
        )
        return users[0] if users else None

    def search(self, domain, fields=None, limit=100):
        if fields is None:
            fields = ["id", "name", "login"]

        return self.service.search_read(
            self.MODEL,
            domain,
            fields=fields,
            limit=limit,
        )

    def all(self, fields=None, limit=100):
        return self.search(
            [],
            fields=fields,
            limit=limit,
        )
