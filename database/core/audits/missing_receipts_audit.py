import re

from database.core.audits.base.base_audit import BaseAudit
from database.core.repositories.pos_order_repository import POSOrderRepository


class MissingReceiptsAudit(BaseAudit):

    code = "missing_receipts"
    name = "Missing POS Receipts Audit"

    def __init__(self):

        super().__init__()
        self.repo = POSOrderRepository()

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
            ],
            limit=limit,
            order="name",
        )

        groups = {}

        for order in orders:

            context = self.build_context(order)

            if context.business_unit is None:
                continue

            key = (
                context.company_id,
                context.business_unit.id,
                context.session_id,
            )

            number = self._receipt_number(order["name"])

            if number is None:
                continue

            groups.setdefault(key, []).append(number)

        results = []

        for key, numbers in groups.items():

            numbers = sorted(set(numbers))

            existing = set(numbers)

            missing = [
                n
                for n in range(numbers[0], numbers[-1] + 1)
                if n not in existing
            ] if numbers else []

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
