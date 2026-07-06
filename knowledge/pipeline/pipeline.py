class KnowledgePipeline:

    def __init__(self):

        self.steps = []

    def register(self, step):

        self.steps.append(step)

    def register_many(self, steps):

        for step in steps:

            self.register(step)

    def run(self, table_name, table_data):

        context = table_data.copy()

        for step in self.steps:

            context = step.process(
                table_name,
                context
            )

        return context
