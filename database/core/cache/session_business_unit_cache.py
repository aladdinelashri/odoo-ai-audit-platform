from database.core.storage.sqlite.database import SQLiteDatabase
from database.core.organization.entity import BusinessUnit


class SessionBusinessUnitCache:

    def __init__(self):

        self.db = SQLiteDatabase()
        self.mapping = {}

    def build(self):

        rows = self.db.query(
            """
            SELECT
                ps.id AS session_id,
                bu.id AS business_unit_id,
                bu.code,
                bu.name,
                bu.source
            FROM pos_sessions ps
            JOIN pos_configs pc
                ON ps.config_id = pc.id
            JOIN business_units bu
                ON bu.id =
                CAST(
                    CASE
                        WHEN instr(pc.iface_available_categ_ids, ',') > 0
                        THEN substr(
                            pc.iface_available_categ_ids,
                            1,
                            instr(pc.iface_available_categ_ids, ',') - 1
                        )
                        ELSE pc.iface_available_categ_ids
                    END
                    AS INTEGER
                )
            """
        )

        for row in rows:

            self.mapping[row["session_id"]] = BusinessUnit(
                id=row["business_unit_id"],
                code=row["code"],
                name=row["name"],
                source=row["source"],
            )

        return self
