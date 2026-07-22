from database.core.audits.base.base_pos_audit import BasePOSAudit
from database.core.cache.cache_loader import CacheLoader
from database.core.repositories.sqlite_pos_payment_repository import (
    SQLitePOSPaymentRepository,
)


class PaymentMethodSummaryAudit(BasePOSAudit):

    code = "payment_method_summary"

    name = "Payment Method Summary Audit"

    def __init__(self):

        super().__init__()

        self.payment_repo = SQLitePOSPaymentRepository()

        self.order_cache = CacheLoader.order_cache()

    def analyze(self):

        payments = self.payment_repo.all_payments()

        summary = {}

        for payment in payments:

            order_context = self.order_cache.orders.get(payment["order_id"])

            if not order_context:
                continue

            business_unit = order_context["business_unit"]

            if business_unit is None:
                continue

            key = (
                order_context["company_id"],
                business_unit.id,
                payment["payment_method"],
            )

            if key not in summary:

                summary[key] = {
                    "company_id": order_context["company_id"],
                    "business_unit_id": business_unit.id,
                    "business_unit_name": business_unit.name,
                    "payment_method": payment["payment_method"],
                    "count": 0,
                    "amount": 0.0,
                }

            summary[key]["count"] += 1
            summary[key]["amount"] += payment["amount"]

        return list(summary.values())
