from datetime import datetime


class AuditScheduler:

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.jobs = []


    def schedule(
        self,
        name,
        interval
    ):

        self.jobs.append({
            "name": name,
            "interval": interval,
            "created_at": datetime.utcnow().isoformat()
        })


    def run(
        self,
        data
    ):

        return self.orchestrator.run(
            data
        )
