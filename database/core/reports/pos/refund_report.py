class RefundPOSReport:

    def build(self, refund):
        return {
            "refund_count": refund.get("count", 0),
            "refund_amount": refund.get("amount", 0)
        }
