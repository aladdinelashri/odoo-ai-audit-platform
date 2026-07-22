from .base_repository import BaseRepository


class POSOrderRepository(BaseRepository):

    TABLE = "pos_orders"

    def paid_orders(self, limit=100):

        return self.search(
            domain=[
                ("state", "=", "paid")
            ],
            fields=[
                "id",
                "order_name",
                "order_date",
                "amount_total",
                "state",
                "session_id",
                "company_id",
            ],
            limit=limit,
            order="order_date DESC",
        )

    def refunded_orders(self, limit=100):

        return self.search(
            fields=[
                "id",
                "order_name",
                "amount_total",
            ],
            limit=limit,
        )

    def orders_between(self, date_from, date_to, limit=1000):

        return self.search(
            domain=[
                ("order_date", ">=", date_from),
                ("order_date", "<=", date_to),
            ],
            fields=[
                "id",
                "order_name",
                "order_date",
                "amount_total",
                "state",
            ],
            limit=limit,
            order="order_date",
        )

    def count_paid(self):

        return self.count(
            [
                ("state", "=", "paid")
            ]
        )
