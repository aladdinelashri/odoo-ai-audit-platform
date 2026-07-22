from .sqlite_base_repository import SQLiteBaseRepository


class SQLiteBusinessUnitRepository(SQLiteBaseRepository):

    TABLE = "business_unit"
