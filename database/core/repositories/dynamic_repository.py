"""
DynamicRepository — Works with ANY Odoo model cached in SQLite.
No hard-coded TABLE. Table name derived from model name automatically.
"""
import json
import sqlite3
from typing import List, Dict, Any, Optional
from config.settings import Settings


class DynamicRepository:
    """
    Generic repository for any Odoo model.
    Table name: account.move -> account_moves
    """

    def __init__(self, model_name: str, db_path: str = None):
        self.model_name = model_name
        self.table_name = model_name.replace(".", "_") + "s"
        self.db_path = db_path or Settings.SQLITE_PATH
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _execute(self, sql: str, params: tuple = ()):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur

    def search(self, domain: list = None, fields: list = None,
               limit: int = None, order: str = None) -> List[Dict[str, Any]]:
        """Odoo-style domain search on SQLite cache."""
        domain = domain or []
        conditions = []
        params = []

        for d in domain:
            if isinstance(d, str):
                continue
            if len(d) != 3:
                continue
            field, op, value = d

            if value is False or value is None:
                if op == "=":
                    conditions.append(f"{field} IS NULL")
                elif op == "!=":
                    conditions.append(f"{field} IS NOT NULL")
                continue

            if op == "=":
                conditions.append(f"{field} = ?")
                params.append(value)
            elif op == "!=":
                conditions.append(f"{field} != ?")
                params.append(value)
            elif op == ">":
                conditions.append(f"{field} > ?")
                params.append(value)
            elif op == "<":
                conditions.append(f"{field} < ?")
                params.append(value)
            elif op == ">=":
                conditions.append(f"{field} >= ?")
                params.append(value)
            elif op == "<=":
                conditions.append(f"{field} <= ?")
                params.append(value)
            elif op == "in":
                if isinstance(value, (list, tuple)) and value:
                    ph = ", ".join("?" * len(value))
                    conditions.append(f"{field} IN ({ph})")
                    params.extend(value)
                else:
                    conditions.append("1=0")
            elif op == "like":
                conditions.append(f"{field} LIKE ?")
                params.append(value)
            elif op == "ilike":
                conditions.append(f"LOWER({field}) LIKE LOWER(?)")
                params.append(value)

        where = " AND ".join(conditions) if conditions else "1=1"
        cols = ", ".join(fields) if fields else "*"
        sql = f"SELECT {cols} FROM {self.table_name} WHERE {where}"
        if order:
            sql += f" ORDER BY {order}"
        if limit:
            sql += f" LIMIT {limit}"

        cur = self._execute(sql, tuple(params))
        rows = [dict(row) for row in cur.fetchall()]

        # Deserialize JSON lists
        for row in rows:
            for k, v in row.items():
                if isinstance(v, str) and v.startswith("["):
                    try:
                        row[k] = json.loads(v)
                    except json.JSONDecodeError:
                        pass
                elif v is None:
                    row[k] = False
        return rows

    def read(self, ids: List[int], fields: list = None) -> List[Dict[str, Any]]:
        if not ids:
            return []
        ph = ", ".join("?" * len(ids))
        cols = ", ".join(fields) if fields else "*"
        sql = f"SELECT {cols} FROM {self.table_name} WHERE id IN ({ph})"
        cur = self._execute(sql, tuple(ids))
        return [dict(row) for row in cur.fetchall()]

    def count(self, domain: list = None) -> int:
        domain = domain or []
        conditions, params = [], []
        for d in domain:
            if len(d) == 3:
                f, op, v = d
                if op == "=":
                    conditions.append(f"{f} = ?")
                    params.append(v)
        where = " AND ".join(conditions) if conditions else "1=1"
        sql = f"SELECT COUNT(*) as count FROM {self.table_name} WHERE {where}"
        cur = self._execute(sql, tuple(params))
        row = cur.fetchone()
        return row["count"] if row else 0
