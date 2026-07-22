from database.core.repositories.sqlite_pos_order_repository import SQLitePOSOrderRepository
from database.core.repositories.sqlite_pos_payment_repository import SQLitePOSPaymentRepository


class AuditDataCache:

    def __init__(self):

        self.order_repo = SQLitePOSOrderRepository()
        self.payment_repo = SQLitePOSPaymentRepository()

        self.orders = {}
        self.payments = []

    def build(self):

        self.orders = {
            order["id"]: dict(order)
            for order in self.order_repo.all_orders()
        }

        self.payments = [
            dict(payment)
            for payment in self.payment_repo.all_payments()
        ]

        return self
