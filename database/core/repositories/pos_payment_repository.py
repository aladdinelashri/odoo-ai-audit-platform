from .base_repository import BaseRepository


class POSPaymentRepository(BaseRepository):

    MODEL = "pos.payment"

    def all_payments(self, limit=100):
        return self.search(
            domain=[],
            fields=[
                "id",
                "payment_date",
                "amount",
                "payment_method_id",
                "pos_order_id",
            ],
            limit=limit,
            order="payment_date desc",
        )

    def payments_between(self, date_from, date_to, limit=1000):
        return self.search(
            domain=[
                ("payment_date", ">=", date_from),
                ("payment_date", "<=", date_to),
            ],
            fields=[
                "id",
                "payment_date",
                "amount",
                "payment_method_id",
                "pos_order_id",
            ],
            limit=limit,
            order="payment_date",
        )

    def by_payment_method(self, payment_method_id, limit=1000):
        return self.search(
            domain=[
                ("payment_method_id", "=", payment_method_id),
            ],
            fields=[
                "id",
                "payment_date",
                "amount",
                "payment_method_id",
                "pos_order_id",
            ],
            limit=limit,
        )

    def count_all(self):
        return self.count([])
