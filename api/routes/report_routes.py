class ReportRoutes:

    def __init__(self, assistant):
        self.assistant = assistant

    def ask(self, question):

        return self.assistant.understand(
            question
        )
