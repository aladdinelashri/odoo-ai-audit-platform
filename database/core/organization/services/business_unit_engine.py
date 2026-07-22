from database.core.cache.session_business_unit_cache import (
    SessionBusinessUnitCache,
)


class BusinessUnitEngine:

    def __init__(self):

        self.cache = SessionBusinessUnitCache().build()

    def resolve(self, order):

        session = order.get("session_id")

        if not session:
            return None

        session_id = session if isinstance(session, int) else session[0]

        return self.cache.mapping.get(session_id)
