from metadata.schema import OdooSchema
from metadata.cache import MetadataCache
from metadata.jsonb import JSONBResolver


class OdooMetadata:

    def __init__(self, language="ar_001"):

        self.schema = OdooSchema()

        self.cache = MetadataCache()

        self.jsonb = JSONBResolver(language)

    def columns(self, table):

        return self.cache.load(table)

    def refresh(self, table):

        return self.cache.refresh(table)

    def jsonb_columns(self, table):

        return self.schema.jsonb_columns(table)

    def has_column(self, table, column):

        return self.schema.has_column(table, column)

    def text(self, value):

        return self.jsonb.text(value)

    def account_code(self, value):

        return self.jsonb.account_code(value)
