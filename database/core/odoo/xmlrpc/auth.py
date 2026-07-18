import xmlrpc.client


class XMLRPCAuth:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password

    def authenticate(self):
        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        return common.authenticate(
            self.db,
            self.username,
            self.password,
            {}
        )
