from .odoo_base_repository import OdooBaseRepository


class OdooPOSPaymentRepository(OdooBaseRepository):

    MODEL = "pos.payment"

    def all(self, limit=100000):

        return self.search(
            fields=[
                "id",
                "company_id",
                "pos_order_id",
                "payment_method_id",
                "amount",
                "payment_date",
            ],
            limit=limit,
            order="id",
        )
