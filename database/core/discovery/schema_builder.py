"""
SQLite Schema Builder — Auto-creates/updates SQLite tables
to match any Odoo model discovered at runtime.
"""
from database.core.storage.sqlite.database import SQLiteDatabase


class SQLiteSchemaBuilder:
    """Builds SQLite tables dynamically from Odoo model metadata."""

    TYPE_MAP = {
        "char": "TEXT",
        "text": "TEXT",
        "html": "TEXT",
        "integer": "INTEGER",
        "float": "REAL",
        "monetary": "REAL",
        "boolean": "INTEGER",
        "date": "TEXT",
        "datetime": "TEXT",
        "many2one": "INTEGER",
        "one2many": "TEXT",
        "many2many": "TEXT",
        "selection": "TEXT",
        "binary": "BLOB",
        "reference": "TEXT",
    }

    def __init__(self, db: SQLiteDatabase = None):
        self.db = db or SQLiteDatabase()

    @staticmethod
    def model_to_table(model_name: str) -> str:
        """account.move -> account_moves"""
        return model_name.replace(".", "_") + "s"

    def build_table(self, model_name: str, fields: list) -> str:
        """
        CREATE TABLE IF NOT EXISTS ... 
        + ALTER TABLE for any new columns discovered later.
        """
        table_name = self.model_to_table(model_name)
        columns = ["id INTEGER PRIMARY KEY"]

        for field in fields:
            if field["name"] == "id":
                continue
            col_name = field["name"]
            col_type = self.TYPE_MAP.get(field["ttype"], "TEXT")
            nullable = "NOT NULL" if field.get("required") else ""
            columns.append(f"{col_name} {col_type} {nullable}".strip())

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.db.execute(sql)

        # Add missing columns (schema evolution per tenant)
        existing = self._get_existing_columns(table_name)
        for field in fields:
            if field["name"] not in existing and field["name"] != "id":
                col_type = self.TYPE_MAP.get(field["ttype"], "TEXT")
                try:
                    self.db.execute(
                        f"ALTER TABLE {table_name} ADD COLUMN {field['name']} {col_type}"
                    )
                except Exception:
                    pass  # Column may already exist or other issue

        return table_name

    def _get_existing_columns(self, table_name: str) -> set:
        try:
            rows = self.db.fetch_all(
                "SELECT name FROM pragma_table_info(?)", (table_name,)
            )
            return {r["name"] if isinstance(r, dict) else r[0] for r in rows}
        except Exception:
            return set()
