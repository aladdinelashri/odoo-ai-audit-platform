class ProductPOSReport:

    def build(self, product):
        return {
            "product": product.get("name"),
            "qty": product.get("qty", 0),
            "sales": product.get("sales", 0)
        }
