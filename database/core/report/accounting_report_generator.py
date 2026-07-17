class AccountingReportGenerator:

    def generate_invoice_report(self, invoices):

        total = 0

        for invoice in invoices:
            total += invoice.get("amount", 0)

        return {
            "type": "invoice",
            "count": len(invoices),
            "total_amount": total
        }


    def generate_tax_report(self, taxes):

        total = 0

        for tax in taxes:
            total += tax.get("amount", 0)

        return {
            "type": "tax",
            "count": len(taxes),
            "total_tax": total
        }
