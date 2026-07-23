# database/core/storage/sqlite/sync_product_products.py

from database.core.odoo.readers.product_product_reader import ProductProductReader
from database.core.storage.sqlite.database import SQLiteDatabase


class ProductProductSynchronizer:

    def __init__(self):

        self.reader = ProductProductReader()
        self.db = SQLiteDatabase()

    def sync(self):

        products = self.reader.all(
            fields=[
                "id",
                "display_name",
                "categ_id",
            ],
            limit=100000,
        )

        rows = []

        for product in products:

            rows.append(
                (
                    product["id"],
                    product["display_name"],
                    product["categ_id"][0] if product.get("categ_id") else None,
                    product["categ_id"][1] if product.get("categ_id") and len(product["categ_id"]) > 1 else None,
                )
            )

        self.db.execute("DELETE FROM product_products")

        self.db.executemany(
            """
            INSERT INTO product_products
            (
                id,
                display_name,
                categ_id,
                categ_name
            )
            VALUES
            (
                ?,?,?,?
            )
            """,
            rows,
        )

        print(f"Product products synchronized: {len(rows)}")

        return len(rows)


if __name__ == "__main__":

    ProductProductSynchronizer().sync()
