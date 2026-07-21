from .daily_report import DailyPOSReport
from .monthly_report import MonthlyPOSReport
from .branch_report import BranchPOSReport
from .product_report import ProductPOSReport
from .category_report import CategoryPOSReport
from .payment_report import PaymentPOSReport


class POSReportRegistry:

    def __init__(self):
        self.reports = {
            "daily": DailyPOSReport(),
            "monthly": MonthlyPOSReport(),
            "branch": BranchPOSReport(),
            "product": ProductPOSReport(),
            "category": CategoryPOSReport(),
            "payment": PaymentPOSReport(),
        }

    def get(self, name):
        return self.reports[name]
