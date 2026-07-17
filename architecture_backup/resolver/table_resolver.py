from database.schema.schema_index import SchemaIndex

from database.ai.reasoning.business_aliases import BUSINESS_ALIASES


class TableResolver:

    def __init__(self):

        self.db = SchemaIndex()

        self.aliases = {}

        self.build()

    # ---------------------------------------------------------

    def build(self):

        # -----------------------------------------
        # Physical Tables
        # -----------------------------------------

        for table in self.db.tables.keys():

            self.aliases[table] = table

            short = table

            for prefix in (

                "account_",
                "res_",
                "pos_",
                "stock_",
                "product_",
                "sale_",
                "purchase_",
                "hr_",
                "mail_",
                "ir_",

            ):

                if short.startswith(prefix):

                    short = short[len(prefix):]

            self.aliases.setdefault(

                short,

                table

            )

        # -----------------------------------------
        # Business Aliases
        # -----------------------------------------

        for table, aliases in BUSINESS_ALIASES.items():

            for alias in aliases:

                self.aliases.setdefault(

                    alias.lower(),

                    table

                )

    # ---------------------------------------------------------

    def resolve(self, name):

        return self.aliases.get(

            name.lower()

        )

    # ---------------------------------------------------------

    def exists(self, name):

        return self.resolve(name) is not None

    # ---------------------------------------------------------

    def all(self):

        return self.aliases
