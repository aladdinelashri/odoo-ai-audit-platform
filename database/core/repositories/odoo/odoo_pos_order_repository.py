from .odoo_base_repository import OdooBaseRepository


class OdooPOSOrderRepository(OdooBaseRepository):

    MODEL = "pos.order"

    def paid_orders(self, limit=100):

        return self.search(
            domain=[
                ("state", "=", "paid")
            ],
            fields=[
                "id",
                "company_id",
                "session_id",
                "partner_id",
                "state",
                "name",
                "date_order",
                "amount_total",
            ],
            limit=limit,
            order="date_order desc",
        )

    def all(self, limit=100000):

        return self.search(
            fields=[
                "id",
                "company_id",
                "session_id",
                "partner_id",
                "state",
                "name",
                "date_order",
                "amount_total",
            ],
            limit=limit,
            order="id",
        )

