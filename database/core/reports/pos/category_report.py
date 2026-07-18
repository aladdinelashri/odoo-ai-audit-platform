class CategoryPOSReport:

    def build(self, category):
        return {
            "category": category.get("name"),
            "sales": category.get("sales", 0),
            "qty": category.get("qty", 0)
        }
