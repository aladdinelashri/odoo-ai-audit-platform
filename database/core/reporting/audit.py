import json
from datetime import datetime
from typing import Optional
from database.core.storage.base_pool import DatabasePool

def log_audit(
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int,
    details: dict,
    db_pool: DatabasePool,
) -> None:
    """Insert an audit log entry into the audit_log table."""
    query = """
        INSERT INTO audit_log (user_id, action, resource_type, resource_id, details, timestamp)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    db_pool.execute_query(query, (user_id, action, resource_type, resource_id, json.dumps(details)))
