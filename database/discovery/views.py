from sqlalchemy import text

from database.discovery.base import BaseDiscovery


class ViewDiscovery(BaseDiscovery):

    def discover(self):

        sql = text("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_schema='public'
            ORDER BY table_name
        """)

        views = []

        with self.engine.connect() as conn:

            rows = conn.execute(sql)

            for row in rows:
                views.append(row.table_name)

        return views
