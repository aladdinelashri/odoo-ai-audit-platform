import sqlite3

from database.core.config.settings import Settings


class SQLiteService:

    FIELD_MAP = {
        "pos_orders": {
            "name": "order_name",
            "date_order": "order_date",
        },
        "pos_payments": {
            "pos_order_id": "order_id",
            "payment_method_id": "payment_method",
        },
    }

    def __init__(self):

        settings = Settings()

        self.conn = sqlite3.connect(settings.sqlite_db_path)
        self.conn.row_factory = sqlite3.Row

    def _map_field(self, table, field):

        return self.FIELD_MAP.get(table, {}).get(field, field)

    def search(self, table, domain=None, fields=None, limit=None, order=None):

        sql = "SELECT "

        if fields:
            mapped = [
                f"{self._map_field(table, f)} AS {f}"
                if self._map_field(table, f) != f
                else f
                for f in fields
            ]
            sql += ", ".join(mapped)
        else:
            sql += "*"

        sql += f" FROM {table}"

        values = []

        if domain:

            clauses = []

            for field, operator, value in domain:

                column = self._map_field(table, field)

                if operator == "=":
                    clauses.append(f"{column} = ?")
                    values.append(value)

                elif operator == "!=":
                    clauses.append(f"{column} != ?")
                    values.append(value)

            if clauses:
                sql += " WHERE " + " AND ".join(clauses)

        if order:

            parts = order.split()

            column = self._map_field(table, parts[0])

            if len(parts) > 1:
                sql += f" ORDER BY {column} {parts[1]}"
            else:
                sql += f" ORDER BY {column}"

        if limit:
            sql += f" LIMIT {limit}"

        return [
            dict(r)
            for r in self.conn.execute(sql, values).fetchall()
        ]

    def read(self, table, ids, fields=None):

        if not ids:
            return []

        sql = "SELECT "

        if fields:
            mapped = [
                f"{self._map_field(table, f)} AS {f}"
                if self._map_field(table, f) != f
                else f
                for f in fields
            ]
            sql += ", ".join(mapped)
        else:
            sql += "*"

        sql += (
            f" FROM {table} WHERE id IN ({','.join('?' * len(ids))})"
        )

        return [
            dict(r)
            for r in self.conn.execute(sql, ids).fetchall()
        ]

    def count(self, table, domain=None):

        sql = f"SELECT COUNT(*) AS total FROM {table}"

        values = []

        if domain:

            clauses = []

            for field, operator, value in domain:

                column = self._map_field(table, field)

                if operator == "=":
                    clauses.append(f"{column} = ?")
                    values.append(value)

            if clauses:
                sql += " WHERE " + " AND ".join(clauses)

        return self.conn.execute(sql, values).fetchone()["total"]
