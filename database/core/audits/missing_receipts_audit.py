import re

from database.core.audits.base.base_pos_audit import BasePOSAudit


class MissingReceiptsAudit(BasePOSAudit):

    code = "missing_receipts"

    name = "Missing Receipts Audit"

    def analyze(self):

        orders = self.get_orders(
            fields=[
                "id",
                "order_name",
                "company_id",
                "session_id",
            ],
            order="order_name",
        )

        numbers = []

        for row in orders:

            name = row.get("order_name") or ""

            match = re.search(r"(\d+)", name)

            if not match:
                continue

            numbers.append(int(match.group(1)))

        if not numbers:
            return []

        numbers = sorted(set(numbers))

        missing = []

        for current, nxt in zip(numbers, numbers[1:]):

            if nxt - current > 1:

                for value in range(current + 1, nxt):

                    missing.append(value)

        return missing
