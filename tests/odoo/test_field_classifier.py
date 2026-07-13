from database.odoo.field_classifier import FieldClassifier

print()
print("=" * 70)
print("FIELD CLASSIFIER")
print("=" * 70)
print()

classifier = FieldClassifier()

tests = [

    "id",
    "name",
    "display_name",
    "date",
    "date_order",
    "invoice_date",
    "partner_id",
    "customer_id",
    "vendor_id",
    "journal_id",
    "company_id",
    "currency_id",
    "product_id",
    "product_template_id",
    "quantity",
    "product_qty",
    "price_unit",
    "list_price",
    "amount_total",
    "amount_tax",
    "amount_residual",
    "state",
    "status",
    "create_date",
    "write_date",
    "activity_date_deadline"

]

for field in tests:

    print(f"{field:30} -> {classifier.classify(field)}")
