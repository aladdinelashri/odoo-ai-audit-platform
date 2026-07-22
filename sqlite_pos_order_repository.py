from .sqlite_base_repository import SQLiteBaseRepository


class SQLitePOSOrderRepository(SQLiteBaseRepository):

    TABLE = "pos_order"
