class KPIEngine:

    def __init__(self):
        self.metrics = {}


    def calculate(
        self,
        name,
        value
    ):

        self.metrics[name] = value

        return {
            "name": name,
            "value": value
        }


    def all(self):

        return self.metrics
