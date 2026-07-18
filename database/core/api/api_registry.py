from .api_engine import APIEngine
from .report_api import ReportAPI
from .dashboard_api import DashboardAPI


class APIRegistry:

    def __init__(self):
        self.routes = {
            "engine": APIEngine(),
            "report": ReportAPI(),
            "dashboard": DashboardAPI(),
        }

    def get(self, name):
        return self.routes[name]
