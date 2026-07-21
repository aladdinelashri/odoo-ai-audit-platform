from database.core.audits.base.base_audit import BaseAudit
from database.core.repositories.pos_order_repository import POSOrderRepository


class BasePOSAudit(BaseAudit):

    def __init__(self):

        super().__init__()

        self.repo = POSOrderRepository()

    def get_orders(
        self,
        domain=None,
        fields=None,
        limit=5000,
        order="id",
    ):

        return self.repo.search(
            domain=domain or [],
            fields=fields or [],
            limit=limit,
            order=order,
        )
