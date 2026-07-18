import xmlrpc.client


class XMLRPCObjectService:

    def __init__(self, url, db, uid, password):
        self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        self.db = db
        self.uid = uid
        self.password = password
