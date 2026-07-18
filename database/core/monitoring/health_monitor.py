from datetime import datetime


class HealthMonitor:

    def __init__(self):
        self.checks = []


    def check(
        self,
        component,
        status
    ):

        result = {
            "component": component,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.checks.append(result)

        return result


    def all(self):

        return self.checks
