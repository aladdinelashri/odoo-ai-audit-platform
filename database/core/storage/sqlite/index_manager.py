"""
Index Manager for SQLite Performance Optimization.
"""

import sqlite3
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class IndexPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class IndexDefinition:
    name: str
    table: str
    columns: List[str]
    priority: IndexPriority
    unique: bool = False
    description: str = ""


class IndexManager:
    RECOMMENDED_INDEXES: List[IndexDefinition] = [
        IndexDefinition("idx_aml_move_id", "account_move_lines", ["move_id"],
            IndexPriority.CRITICAL, description="Eliminates N+1 when joining moves to lines"),
        IndexDefinition("idx_aml_account_id", "account_move_lines", ["account_id"],
            IndexPriority.CRITICAL, description="Fast lookup of lines by account"),
        IndexDefinition("idx_aml_tax_line_id", "account_move_lines", ["tax_line_id"],
            IndexPriority.HIGH, description="Tax validation queries"),
        IndexDefinition("idx_aml_date", "account_move_lines", ["date"],
            IndexPriority.HIGH, description="Date-range filtering"),
        IndexDefinition("idx_am_state", "account_moves", ["state"],
            IndexPriority.CRITICAL, description="Filter by posted/draft/cancel state"),
        IndexDefinition("idx_am_date", "account_moves", ["date"],
            IndexPriority.HIGH, description="Date-range filtering for audits"),
        IndexDefinition("idx_am_journal_id", "account_moves", ["journal_id"],
            IndexPriority.HIGH, description="Journal-specific queries"),
        IndexDefinition("idx_am_name", "account_moves", ["name"],
            IndexPriority.MEDIUM, description="Sequence gap detection"),
        IndexDefinition("idx_am_partner_id", "account_moves", ["partner_id"],
            IndexPriority.MEDIUM, description="Partner validation"),
        IndexDefinition("idx_aa_type", "account_accounts", ["account_type"],
            IndexPriority.CRITICAL, description="Filter by account type"),
        IndexDefinition("idx_aa_code", "account_accounts", ["code"],
            IndexPriority.HIGH, description="Account code lookups"),
        IndexDefinition("idx_aa_parent_id", "account_accounts", ["parent_id"],
            IndexPriority.MEDIUM, description="Parent-child hierarchy queries"),
        IndexDefinition("idx_aj_type", "account_journals", ["type"],
            IndexPriority.MEDIUM, description="Filter by journal type"),
        IndexDefinition("idx_po_session_id", "pos_orders", ["session_id"],
            IndexPriority.HIGH, description="Session-based POS queries"),
        IndexDefinition("idx_po_date", "pos_orders", ["date_order"],
            IndexPriority.HIGH, description="Date-range POS queries"),
    ]
    
    def __init__(self, db_path: str = "database/storage/audit.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self) -> sqlite3.Connection:
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA journal_mode = WAL")
            self.conn.execute("PRAGMA synchronous = NORMAL")
        return self.conn
    
    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def create_index(self, index_def: IndexDefinition, if_not_exists: bool = True) -> bool:
        exists_clause = "IF NOT EXISTS" if if_not_exists else ""
        unique_clause = "UNIQUE" if index_def.unique else ""
        columns_str = ", ".join(index_def.columns)
        sql = f"CREATE {unique_clause} INDEX {exists_clause} {index_def.name} ON {index_def.table} ({columns_str})"
        try:
            self.connect().execute(sql)
            self.connect().commit()
            logger.info(f"Created index: {index_def.name}")
            return True
        except sqlite3.OperationalError as e:
            if "already exists" in str(e):
                return False
            raise
    
    def create_all_recommended(self) -> Dict[str, bool]:
        results = {}
        for idx in self.RECOMMENDED_INDEXES:
            results[idx.name] = self.create_index(idx)
        return results
    
    def create_critical_only(self) -> Dict[str, bool]:
        results = {}
        for idx in self.RECOMMENDED_INDEXES:
            if idx.priority == IndexPriority.CRITICAL:
                results[idx.name] = self.create_index(idx)
        return results
    
    def list_existing_indexes(self, table_name: Optional[str] = None) -> List[Dict[str, str]]:
        if table_name:
            cursor = self.connect().execute(
                "SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name=?",
                (table_name,))
        else:
            cursor = self.connect().execute(
                "SELECT name, sql, tbl_name as table_name FROM sqlite_master WHERE type='index'")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_missing_critical_indexes(self) -> List[IndexDefinition]:
        existing = {idx["name"] for idx in self.list_existing_indexes()}
        return [idx for idx in self.RECOMMENDED_INDEXES 
                if idx.priority == IndexPriority.CRITICAL and idx.name not in existing]


def setup_critical_indexes(db_path: str = "database/storage/audit.db") -> Dict[str, bool]:
    manager = IndexManager(db_path)
    try:
        return manager.create_critical_only()
    finally:
        manager.close()
