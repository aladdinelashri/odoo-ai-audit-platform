import re

from database.core.audits.base.base_audit import BaseAudit
from database.core.organization.services import OrganizationService
from database.core.repositories.pos_order_repository import POSOrderRepository


class MissingReceiptsAudit(BaseAudit):

    code = "missing_receipts"
    name = "Missing POS Receipts Audit"

    def __init__(self):

        self.repo = POSOrderRepository()
        self.organization_service = OrganizationService()

    @staticmethod
    def _receipt_number(receipt_name):

        if not receipt_name:
            return None

        match = re.search(r"(\d+)$", receipt_name)

        if not match:
            return None

        return int(match.group(1))

    def analyze(self, limit=5000):

        orders = self.repo.search(
            domain=[
                ("state", "=", "paid"),
            ],
            fields=[
                "id",
                "name",
                "date_order",
                "session_id",
                "company_id",
                "amount_total",
            ],
            limit=limit,
            order="name",
        )

        groups = {}

        for order in orders:

            business_unit = self.organization_service.resolve(order)

            key = (
                order["company_id"][0] if order.get("company_id") else 0,
                business_unit.id if business_unit else 0,
                order["session_id"][0] if order.get("session_id") else 0,
            )

            number = self._receipt_number(order["name"])

            if number is None:
                continue

            groups.setdefault(key, []).append(number)

        results = []

        for key, numbers in groups.items():

            numbers = sorted(set(numbers))

            missing = []

            if numbers:

                existing = set(numbers)

                for n in range(numbers[0], numbers[-1] + 1):

                    if n not in existing:
                        missing.append(n)

            results.append(
                {
                    "company_id": key[0],
                    "business_unit_id": key[1],
                    "session_id": key[2],
                    "first_receipt": numbers[0] if numbers else None,
                    "last_receipt": numbers[-1] if numbers else None,
                    "existing_receipts": len(numbers),
                    "missing_receipts": len(missing),
                    "missing_numbers": missing,
                }
            )

        return results
