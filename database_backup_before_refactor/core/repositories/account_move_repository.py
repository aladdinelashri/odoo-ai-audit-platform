from .base_repository import BaseRepository


class AccountMoveRepository(BaseRepository):

    MODEL = "account.move"

    def posted_moves(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "posted")
            ],
            fields=[
                "id",
                "name",
                "date",
                "move_type",
                "journal_id",
                "company_id",
                "state",
            ],
            limit=limit,
            order="date desc",
        )

    def cancelled_moves(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "cancel")
            ],
            fields=[
                "id",
                "name",
                "date",
                "move_type",
                "state",
            ],
            limit=limit,
        )

    def draft_moves(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "draft")
            ],
            fields=[
                "id",
                "name",
                "date",
                "move_type",
                "state",
            ],
            limit=limit,
        )

    def moves_between(self, date_from, date_to, limit=1000):
        return self.search(
            domain=[
                ("date", ">=", date_from),
                ("date", "<=", date_to),
            ],
            fields=[
                "id",
                "name",
                "date",
                "move_type",
                "state",
            ],
            limit=limit,
            order="date",
        )

    def count_posted(self):
        return self.count(
            [
                ("state", "=", "posted")
            ]
        )
