from metadata.odoo import OdooMetadata


class JSONFormatter:

    def __init__(self, language="ar_001"):

        self.metadata = OdooMetadata(language)

    def format_row(self, row):

        result = {}

        for key, value in row.items():

            if isinstance(value, dict):

                if key.endswith("code") or key.endswith("_code"):

                    result[key] = self.metadata.account_code(value)

                else:

                    result[key] = self.metadata.text(value)

            else:

                result[key] = value

        return result

    def format_rows(self, rows):

        return [

            self.format_row(row)

            for row in rows

        ]
