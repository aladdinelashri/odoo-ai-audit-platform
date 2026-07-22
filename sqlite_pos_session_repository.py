from .sqlite_base_repository import SQLiteBaseRepository


class SQLitePOSSessionRepository(SQLiteBaseRepository):

    TABLE = "pos_session"
