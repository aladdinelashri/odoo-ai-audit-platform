class POSKPICalculator:

    def calculate(self, orders):

        total_sales = sum(
            order.get("amount_total", 0)
            for order in orders
        )

        receipt_count = len(orders)

        average_sale = (
            total_sales / receipt_count
            if receipt_count else 0
        )

        return {
            "total_sales": total_sales,
            "receipt_count": receipt_count,
            "average_sale": average_sale
        }
