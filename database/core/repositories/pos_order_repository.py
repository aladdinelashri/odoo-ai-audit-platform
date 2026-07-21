from .base_repository import BaseRepository


class POSOrderRepository(BaseRepository):

    MODEL = "pos.order"

    def paid_orders(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "paid")
            ],
            fields=[
                "id",
                "name",
                "date_order",
                "partner_id",
                "amount_total",
                "state",
                "session_id",
                "company_id",
            ],
            limit=limit,
            order="date_order desc",
        )

    def refunded_orders(self, limit=100):
        return self.search(
            domain=[
                ("refund_order_ids", "!=", False)
            ],
            fields=[
                "id",
                "name",
                "amount_total",
                "refund_order_ids",
            ],
            limit=limit,
        )

    def orders_between(self, date_from, date_to, limit=1000):
        return self.search(
            domain=[
                ("date_order", ">=", date_from),
                ("date_order", "<=", date_to),
            ],
            fields=[
                "id",
                "name",
                "date_order",
                "amount_total",
                "state",
            ],
            limit=limit,
            order="date_order",
        )

    def count_paid(self):
        return self.count(
            [
                ("state", "=", "paid")
            ]
        )
