import json
from pathlib import Path

from database.schema.schema_index import SchemaIndex


class CatalogBuilder:

    def __init__(self):

        self.db = SchemaIndex()

    # ---------------------------------------------------------

    def infer_roles(self, columns):

        roles = {}

        for column in columns:

            name = column["column_name"].lower()

            if name in (
                "amount_total",
                "price_total",
                "balance",
                "list_price",
                "standard_price",
                "price_unit",
            ):
                roles.setdefault("monetary_total", []).append(name)

            elif name in (
                "amount_tax",
                "tax_amount",
            ):
                roles.setdefault("tax_amount", []).append(name)

            elif name in (
                "amount_residual",
            ):
                roles.setdefault("residual_amount", []).append(name)

            elif name in (
                "partner_id",
            ):
                roles.setdefault("business_partner", []).append(name)

            elif name in (
                "date",
                "date_order",
                "invoice_date",
            ):
                roles.setdefault("document_date", []).append(name)

            elif name in (
                "name",
                "move_name",
                "number",
            ):
                roles.setdefault("document_number", []).append(name)

            elif name == "state":

                roles.setdefault("document_state", []).append(name)

        return roles

    # ---------------------------------------------------------

    def build(self):

        catalog = {}

        for table in self.db.table_names():

            columns = self.db.columns(table)

            catalog[table] = {

                "columns": columns,

                "relations": self.db.relations_from(table),

                "semantic_roles": self.infer_roles(columns)

            }

        output = Path("database/catalog/catalog.json")

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                catalog,
                f,
                ensure_ascii=False,
                indent=4
            )

        print()
        print("=" * 70)
        print("Catalog Builder")
        print("=" * 70)
        print()
        print(f"Tables : {len(catalog)}")
        print(f"Saved  : {output}")
        print()

        return catalog


if __name__ == "__main__":

    CatalogBuilder().build()
