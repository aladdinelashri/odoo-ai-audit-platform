from .sqlite_base_repository import SQLiteBaseRepository


class SQLitePOSPaymentRepository(SQLiteBaseRepository):

    TABLE = "pos_payment"
