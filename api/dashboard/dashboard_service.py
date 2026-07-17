class DashboardService:

    def __init__(self, report_generator):
        self.report_generator = report_generator

    def get_summary(self, data):

        return {
            "summary": self.report_generator.build(
                "Dashboard Summary",
                data
            )
        }
