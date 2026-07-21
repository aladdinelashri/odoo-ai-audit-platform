class AuditPipeline:

    def __init__(
        self,
        query_engine,
        rule_engine
    ):
        self.query_engine = query_engine
        self.rule_engine = rule_engine


    def run(
        self,
        model,
        fields
    ):

        data = self.query_engine.fetch(
            model,
            fields
        )

        return self.rule_engine.evaluate(
            data
        )
