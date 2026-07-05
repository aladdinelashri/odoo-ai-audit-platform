from sqlalchemy import text

from database.discovery.base import BaseDiscovery


class ConstraintDiscovery(BaseDiscovery):

    def discover(self):

        sql = text("""
            SELECT
                c.relname AS table_name,
                con.conname AS constraint_name,
                con.contype AS constraint_type
            FROM pg_constraint con
            JOIN pg_class c
                ON c.oid = con.conrelid
            JOIN pg_namespace n
                ON n.oid = c.relnamespace
            WHERE n.nspname = 'public'
            ORDER BY c.relname, con.conname;
        """)

        result = {}

        with self.engine.connect() as conn:

            rows = conn.execute(sql)

            for row in rows:

                table = row.table_name

                if table not in result:
                    result[table] = []

                constraint_type = {
                    "p": "PRIMARY KEY",
                    "f": "FOREIGN KEY",
                    "u": "UNIQUE",
                    "c": "CHECK",
                    "x": "EXCLUSION",
                }.get(row.constraint_type, row.constraint_type)

                result[table].append(
                    {
                        "name": row.constraint_name,
                        "type": constraint_type,
                    }
                )

        return result
