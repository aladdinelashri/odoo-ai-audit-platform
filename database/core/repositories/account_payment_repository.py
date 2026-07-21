from .base_repository import BaseRepository


class AccountPaymentRepository(BaseRepository):

    MODEL = "account.payment"

    def posted(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "posted")
            ],
            fields=[
                "id",
                "name",
                "date",
                "payment_type",
                "partner_type",
                "amount",
                "journal_id",
                "state",
            ],
            limit=limit,
            order="date desc",
        )

    def inbound(self, limit=100):
        return self.search(
            domain=[
                ("payment_type", "=", "inbound")
            ],
            fields=[
                "id",
                "name",
                "date",
                "amount",
                "partner_id",
                "state",
            ],
            limit=limit,
        )

    def outbound(self, limit=100):
        return self.search(
            domain=[
                ("payment_type", "=", "outbound")
            ],
            fields=[
                "id",
                "name",
                "date",
                "amount",
                "partner_id",
                "state",
            ],
            limit=limit,
        )

    def count_posted(self):
        return self.count(
            [
                ("state", "=", "posted")
            ]
        )
