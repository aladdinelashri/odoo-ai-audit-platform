"""
AST validation and whitelist enforcement.
Supports both simple and complex AST formats.
Dynamically loads table/column whitelist from the SQLite Odoo cache.
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, ValidationError, model_validator

# ---------- Dynamic Whitelist Loading from SQLite ----------
def _load_sqlite_schema(db_path: str = "database/storage/audit.db") -> Dict[str, set]:
    """
    Read table and column names from the SQLite Odoo cache.
    Falls back to empty dict if SQLite is not available.
    """
    schema: Dict[str, set] = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables (excluding SQLite internals and sync metadata)
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%' 
            AND name NOT LIKE '_sync_meta'
            AND name NOT LIKE 'alembic_%'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = {row[1] for row in cursor.fetchall()}
            schema[table] = columns
            
        conn.close()
    except Exception:
        pass
    
    return schema


# Load schema at import time
_SQLITE_SCHEMA = _load_sqlite_schema()

# Audit platform tables (always allowed, in PostgreSQL)
_AUDIT_TABLES = {
    "users", "reports", "report_executions", "audit_log"
}

_AUDIT_COLUMNS = {
    "users": {"id", "username", "hashed_password", "role", "created_at"},
    "reports": {"id", "name", "description", "query_ast", "parameters", "schedule",
                "export_format", "recipients", "status", "created_by", "created_at",
                "updated_at", "last_run", "next_run"},
    "report_executions": {"id", "report_id", "executed_at", "parameters", "result_size",
                          "execution_time_ms", "error", "output_url"},
    "audit_log": {"id", "user_id", "action", "resource_type", "resource_id", "details", "timestamp"},
}

# Merge: audit tables + dynamically discovered SQLite Odoo tables
ALLOWED_TABLES = _AUDIT_TABLES | set(_SQLITE_SCHEMA.keys())
ALLOWED_COLUMNS = {**_AUDIT_COLUMNS, **_SQLITE_SCHEMA}

ALLOWED_OPERATORS = {"=", "!=", ">", "<", ">=", "<=", "LIKE", "IN", "NOT IN", "IS NULL", "IS NOT NULL", "BETWEEN"}
ALLOWED_LOGICAL = {"AND", "OR"}


# ---------- Pydantic models for complex AST ----------
class SelectItem(BaseModel):
    column: str
    alias: Optional[str] = None

class FromItem(BaseModel):
    table: str
    alias: Optional[str] = None

class WhereClause(BaseModel):
    left: str
    operator: str
    right: Any
    logical: Optional[str] = None

class OrderByItem(BaseModel):
    column: str
    direction: Optional[str] = "ASC"

class QueryAST(BaseModel):
    select: List[Union[str, SelectItem]]
    from_: FromItem = Field(alias="from")
    where: Optional[Union[Dict, List[Dict]]] = None
    order_by: Optional[List[OrderByItem]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    class Config:
        populate_by_name = True

# ---------- Simple AST format ----------
class SimpleSelectAST(BaseModel):
    type: str = "select"
    table: Optional[str] = None
    from_: Optional[str] = Field(default=None, alias="from")
    columns: List[str]
    where: Optional[Dict] = None
    order_by: Optional[List[str]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    @model_validator(mode="after")
    def normalize_table(self):
        if self.table and self.from_:
            raise ValueError("Provide either 'table' or 'from', not both")
        if self.from_ and not self.table:
            self.table = self.from_
        if not self.table:
            raise ValueError("Simple AST requires 'table' or 'from' field")
        return self

# ---------- Validation function ----------
def validate_ast(ast_dict: Dict[str, Any]) -> bool:
    if not isinstance(ast_dict, dict):
        raise ValueError("AST must be a dictionary")

    has_columns = "columns" in ast_dict
    from_is_string = isinstance(ast_dict.get("from"), str)
    has_table_string = isinstance(ast_dict.get("table"), str)
    has_select = "select" in ast_dict
    from_is_dict = isinstance(ast_dict.get("from"), dict)

    if has_columns and (from_is_string or has_table_string):
        return _validate_simple_ast(ast_dict)
    if has_select and from_is_dict:
        return _validate_complex_ast(ast_dict)

    try:
        return _validate_simple_ast(ast_dict)
    except ValueError:
        pass
    try:
        return _validate_complex_ast(ast_dict)
    except ValueError:
        pass

    raise ValueError(
        "AST validation failed: unable to determine AST format. "
        "Expected simple format ('type', 'from'/'table' as string, 'columns') "
        "or complex format ('select', 'from' as dict)."
    )

def _validate_simple_ast(ast_dict: Dict[str, Any]) -> bool:
    try:
        parsed = SimpleSelectAST(**ast_dict)
    except ValidationError as e:
        raise ValueError(f"AST validation failed (simple format): {e}")

    if parsed.table not in ALLOWED_TABLES:
        raise ValueError(f"Table '{parsed.table}' not allowed. Allowed: {ALLOWED_TABLES}")

    allowed_cols = ALLOWED_COLUMNS.get(parsed.table, set())
    for col in parsed.columns:
        if col != "*" and col not in allowed_cols:
            raise ValueError(f"Column '{col}' not allowed for table '{parsed.table}'. Allowed: {allowed_cols}")

    if parsed.where:
        _validate_where(parsed.where)

    return True

def _validate_complex_ast(ast_dict: Dict[str, Any]) -> bool:
    try:
        parsed = QueryAST(**ast_dict)
    except ValidationError as e:
        raise ValueError(f"AST validation failed (complex format): {e}")

    if parsed.from_.table not in ALLOWED_TABLES:
        raise ValueError(f"Table '{parsed.from_.table}' not allowed. Allowed: {ALLOWED_TABLES}")

    allowed_cols = ALLOWED_COLUMNS.get(parsed.from_.table, set())
    for item in parsed.select:
        col = item if isinstance(item, str) else item.column
        if col != "*" and col not in allowed_cols:
            raise ValueError(f"Column '{col}' not allowed for table '{parsed.from_.table}'. Allowed: {allowed_cols}")

    if parsed.where:
        _validate_where(parsed.where)

    return True

def _validate_where(where_clause: Union[Dict, List[Dict]]):
    if isinstance(where_clause, dict):
        if "logical" in where_clause:
            if where_clause["logical"] not in ALLOWED_LOGICAL:
                raise ValueError(f"Invalid logical operator: {where_clause['logical']}")
            if "conditions" in where_clause:
                for cond in where_clause["conditions"]:
                    _validate_where(cond)
        else:
            if "left" not in where_clause or "operator" not in where_clause:
                raise ValueError("WHERE condition missing 'left' or 'operator'")
            if where_clause["operator"] not in ALLOWED_OPERATORS:
                raise ValueError(f"Invalid operator: {where_clause['operator']}")
    elif isinstance(where_clause, list):
        for cond in where_clause:
            _validate_where(cond)
    else:
        raise ValueError("Invalid WHERE clause structure")

# ---------- Converter ----------
def simple_to_complex(simple_ast: Dict[str, Any]) -> Dict[str, Any]:
    table_name = simple_ast.get("table") or simple_ast.get("from")
    if not table_name:
        raise ValueError("Simple AST must contain 'table' or 'from'")
    return {
        "select": simple_ast["columns"],
        "from": {"table": table_name},
        "where": simple_ast.get("where"),
        "order_by": [{"column": c} for c in simple_ast.get("order_by", [])] if simple_ast.get("order_by") else None,
        "limit": simple_ast.get("limit"),
        "offset": simple_ast.get("offset"),
    }

def convert_to_complex(ast_dict: Dict[str, Any]) -> Dict[str, Any]:
    is_simple = "columns" in ast_dict and (isinstance(ast_dict.get("from"), str) or "table" in ast_dict)
    if is_simple:
        return simple_to_complex(ast_dict)
    return ast_dict
