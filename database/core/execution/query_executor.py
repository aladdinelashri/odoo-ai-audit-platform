class QueryExecutor:

    def __init__(self, connection):
        self.connection = connection

    def execute(self, sql):

        return self.connection.fetch_all(sql)
