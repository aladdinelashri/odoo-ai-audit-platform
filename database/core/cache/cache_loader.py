from database.core.cache.audit_data_cache import AuditDataCache
from database.core.cache.order_context_cache import OrderContextCache
from database.core.cache.session_business_unit_cache import SessionBusinessUnitCache


class CacheLoader:

    _audit_cache = None
    _session_cache = None
    _order_cache = None

    @classmethod
    def audit_cache(cls):
        if cls._audit_cache is None:
            cls._audit_cache = AuditDataCache().build()
        return cls._audit_cache

    @classmethod
    def session_cache(cls):
        if cls._session_cache is None:
            cls._session_cache = SessionBusinessUnitCache().build()
        return cls._session_cache

    @classmethod
    def order_cache(cls):
        if cls._order_cache is None:
            cls._order_cache = OrderContextCache().build()
        return cls._order_cache
