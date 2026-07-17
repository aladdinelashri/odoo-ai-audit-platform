class OdooDataAdapter:

    def __init__(self, connector):
        self.connector = connector


    def fetch_model_data(
        self,
        model,
        fields
    ):

        return self.connector.execute_read(
            model,
            fields
        )


    def count_records(
        self,
        model,
        domain=None
    ):

        return self.connector.search_count(
            model,
            domain
        )
