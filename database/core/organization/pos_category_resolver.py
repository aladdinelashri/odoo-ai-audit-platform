from database.core.repositories.pos_config_repository import POSConfigRepository

from .entity import BusinessUnit
from .resolver import BusinessUnitResolver


class CategoryBusinessUnitResolver(BusinessUnitResolver):

    def __init__(self, config):

        self.config = config
        self.pos_config_repo = POSConfigRepository()

    def resolve(self, order):

        session = order.get("session_id")

        if not session:
            return None

        session_id = session[0]

        configs = self.pos_config_repo.search(
            [
                ("current_session_id", "=", session_id),
            ],
            fields=[
                "id",
                "name",
                "iface_available_categ_ids",
            ],
            limit=1,
        )

        if not configs:
            return None

        config = configs[0]

        categories = config.get("iface_available_categ_ids") or []

        if not categories:
            return None

        category_id = categories[0]

        return BusinessUnit(
            id=category_id,
            code=str(category_id),
            name=f"POS Category {category_id}",
            source=self.config["model"],
        )
