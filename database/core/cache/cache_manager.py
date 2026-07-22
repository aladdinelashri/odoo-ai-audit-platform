from database.core.repositories.pos_session_repository import POSSessionRepository
from database.core.repositories.pos_config_repository import POSConfigRepository
from database.core.repositories.pos_category_repository import POSCategoryRepository


class CacheManager:

    def __init__(self):

        self.session_repo = POSSessionRepository()
        self.config_repo = POSConfigRepository()
        self.category_repo = POSCategoryRepository()

        self.sessions = {}
        self.configs = {}
        self.categories = {}

    def build(self):

        self.sessions = {
            r["id"]: r
            for r in self.session_repo.search(
                fields=[
                    "id",
                    "config_id",
                ],
                limit=100000,
            )
        }

        self.configs = {
            r["id"]: r
            for r in self.config_repo.search(
                fields=[
                    "id",
                    "company_id",
                    "name",
                ],
                limit=100000,
            )
        }

        self.categories = {
            r["id"]: r
            for r in self.category_repo.search(
                fields=[
                    "id",
                    "name",
                ],
                limit=100000,
            )
        }

        return self
