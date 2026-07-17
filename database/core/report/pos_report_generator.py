class POSReportGenerator:

    def generate_sales_report(self, orders):

        total = 0

        for order in orders:
            total += order.get("amount", 0)

        return {
            "type": "sales",
            "orders_count": len(orders),
            "total_sales": total
        }


    def generate_receipt_report(self, receipts):

        return {
            "type": "receipts",
            "count": len(receipts),
            "missing": self._find_missing(receipts)
        }


    def _find_missing(self, receipts):

        missing = []

        for i in range(len(receipts)-1):
            gap = receipts[i+1] - receipts[i]

            if gap > 1:
                missing.extend(
                    range(
                        receipts[i]+1,
                        receipts[i+1]
                    )
                )

        return missing
