class OdooConnector:

    def __init__(self, connection):
        self.connection = connection


    def execute_read(self, model, fields):

        return self.connection.read(
            model,
            fields
        )


    def search_count(self, model, domain=None):

        return self.connection.count(
            model,
            domain or []
        )
