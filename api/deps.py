from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from database.core.storage.base_pool import DatabasePool

# Shared rate limiter instance (per IP)
limiter = Limiter(key_func=get_remote_address)

def get_db_pool(request: Request) -> DatabasePool:
    """Dependency that returns the database pool from the app state."""
    return request.app.state.db_pool
