from .base_repository import BaseRepository


class POSSessionRepository(BaseRepository):

    MODEL = "pos.session"

    def opened_sessions(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "opened")
            ],
            fields=[
                "id",
                "name",
                "config_id",
                "company_id",
                "state",
                "start_at",
            ],
            limit=limit,
            order="start_at desc",
        )

    def closed_sessions(self, limit=100):
        return self.search(
            domain=[
                ("state", "=", "closed")
            ],
            fields=[
                "id",
                "name",
                "config_id",
                "company_id",
                "state",
                "start_at",
                "stop_at",
            ],
            limit=limit,
            order="stop_at desc",
        )

    def sessions_between(self, date_from, date_to, limit=1000):
        return self.search(
            domain=[
                ("start_at", ">=", date_from),
                ("start_at", "<=", date_to),
            ],
            fields=[
                "id",
                "name",
                "state",
                "start_at",
                "stop_at",
            ],
            limit=limit,
            order="start_at",
        )

    def count_opened(self):
        return self.count(
            [
                ("state", "=", "opened")
            ]
        )
