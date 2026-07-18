class QueryEngine:

    def __init__(self, adapter):
        self.adapter = adapter


    def fetch(
        self,
        model,
        fields
    ):

        return self.adapter.fetch_model_data(
            model,
            fields
        )


    def count(
        self,
        model,
        domain=None
    ):

        return self.adapter.count_records(
            model,
            domain
        )
