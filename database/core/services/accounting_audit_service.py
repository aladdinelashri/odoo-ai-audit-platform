from database.core.repositories.account_move_repository import AccountMoveRepository
from database.core.repositories.account_payment_repository import (
    AccountPaymentRepository,
)


class AccountingAuditService:

    def __init__(self):
        self.moves = AccountMoveRepository()
        self.payments = AccountPaymentRepository()

    def summary(self):

        return {
            "posted_moves": self.moves.count_posted(),
            "posted_payments": self.payments.count_posted(),
        }

    def latest_posted_move(self):
        return self.moves.posted_moves(limit=1)

    def latest_payment(self):
        return self.payments.posted(limit=1)
