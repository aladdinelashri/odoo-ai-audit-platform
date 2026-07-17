from database.sql.sql_executor import SQLExecutor


class SchemaExtractor:

    def __init__(self):

        self.executor = SQLExecutor()

    # ---------------------------------------------------------

    def tables(self):

        sql = """
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        ORDER BY table_name
        """

        return self.executor.execute(sql)

    # ---------------------------------------------------------

    def columns(self, table):

        sql = """
        SELECT
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema='public'
        AND table_name=%s
        ORDER BY ordinal_position
        """

        return self.executor.execute(sql, (table,))

    # ---------------------------------------------------------

    def foreign_keys(self, table):

        sql = """

        SELECT

            kcu.column_name,

            ccu.table_name AS foreign_table,

            ccu.column_name AS foreign_column

        FROM information_schema.table_constraints tc

        JOIN information_schema.key_column_usage kcu

            ON tc.constraint_name = kcu.constraint_name

        JOIN information_schema.constraint_column_usage ccu

            ON ccu.constraint_name = tc.constraint_name

        WHERE tc.constraint_type = 'FOREIGN KEY'

        AND tc.table_schema='public'

        AND tc.table_name=%s

        ORDER BY kcu.column_name

        """

        return self.executor.execute(sql, (table,))
