from database.core.organization.entity import BusinessUnit
from database.core.storage.sqlite.database import SQLiteDatabase


class SQLiteContextBuilder:

    def __init__(self):
        self.db = SQLiteDatabase()

    def build(self, order_id):

        row = self.db.query_one(
            """
            SELECT
                o.company_id,
                o.session_id,
                m.business_unit_id,
                m.business_unit_name
            FROM pos_orders o
            LEFT JOIN session_business_unit_map m
                ON o.session_id = m.session_id
            WHERE o.id = ?
            """,
            (order_id,),
        )

        if row is None:
            return None

        return {
            "company_id": row["company_id"],
            "session_id": row["session_id"],
            "business_unit": BusinessUnit(
                id=row["business_unit_id"],
                code=str(row["business_unit_id"]),
                name=row["business_unit_name"],
                source="sqlite",
            ),
        }
