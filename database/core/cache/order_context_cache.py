from database.core.cache.audit_data_cache import AuditDataCache
from database.core.cache.session_business_unit_cache import SessionBusinessUnitCache


class OrderContextCache:

    def __init__(self):

        self.audit_cache = AuditDataCache().build()
        self.session_cache = SessionBusinessUnitCache().build()

        self.orders = {}

    def build(self):

        for order in self.audit_cache.orders.values():

            session_id = order["session_id"]

            business_unit = self.session_cache.mapping.get(session_id)

            self.orders[order["id"]] = {
                "order": order,
                "business_unit": business_unit,
                "company_id": order["company_id"],
                "session_id": session_id,
            }

        return self
