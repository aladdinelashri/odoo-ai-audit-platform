from .dashboard_engine import DashboardEngine
from .kpi_dashboard import KPIDashboard
from .branch_dashboard import BranchDashboard


class DashboardRegistry:

    def __init__(self):
        self.items = {
            "engine": DashboardEngine(),
            "kpi": KPIDashboard(),
            "branch": BranchDashboard(),
        }

    def get(self, name):
        return self.items[name]
