from database.core.repositories.pos_order_repository import POSOrderRepository
from database.core.repositories.pos_payment_repository import POSPaymentRepository
from database.core.repositories.pos_session_repository import POSSessionRepository


class POSAuditService:

    def __init__(self):
        self.orders = POSOrderRepository()
        self.payments = POSPaymentRepository()
        self.sessions = POSSessionRepository()

    def summary(self):

        return {
            "paid_orders": self.orders.count_paid(),
            "payments": self.payments.count_all(),
            "opened_sessions": self.sessions.count_opened(),
        }

    def latest_paid_order(self):
        return self.orders.paid_orders(limit=1)

    def latest_payment(self):
        return self.payments.all_payments(limit=1)

    def latest_session(self):
        return self.sessions.opened_sessions(limit=1)
