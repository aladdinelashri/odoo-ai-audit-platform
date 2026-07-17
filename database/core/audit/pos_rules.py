class POSAuditRules:

    def check_missing_receipts(self, receipts):

        missing = []

        for i in range(len(receipts) - 1):
            current = receipts[i]
            next_value = receipts[i + 1]

            if next_value - current > 1:
                missing.extend(
                    range(current + 1, next_value)
                )

        return missing


    def check_refunds(self, orders):

        return [
            order for order in orders
            if order.get("state") == "refund"
        ]
