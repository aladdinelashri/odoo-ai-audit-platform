class ProductDashboard:

    def build(self, product):
        return {
            "product": product.get("name"),
            "sales": product.get("sales", 0),
            "qty": product.get("qty", 0)
        }
