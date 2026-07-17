class OrderBuilder:

    def __init__(self):

        self.orders = []

    def add(self, field, direction="ASC"):

        self.orders.append(

            f"{field} {direction}"

        )

    def sql(self):

        if not self.orders:

            return ""

        return "ORDER BY\n    " + ", ".join(self.orders)
