from .odoo_base_repository import OdooBaseRepository


class OdooPOSSessionRepository(OdooBaseRepository):

    MODEL = "pos.session"

    def all(self, limit=100000):

        return self.search(
            fields=[
                "id",
                "company_id",
                "config_id",
                "name",
                "state",
                "start_at",
                "stop_at",
            ],
            limit=limit,
            order="id",
        )
