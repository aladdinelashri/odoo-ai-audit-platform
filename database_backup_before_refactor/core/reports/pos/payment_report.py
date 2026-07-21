class PaymentPOSReport:

    def build(self, payment):
        return {
            "method": payment.get("method"),
            "amount": payment.get("amount", 0),
            "count": payment.get("count", 0)
        }
