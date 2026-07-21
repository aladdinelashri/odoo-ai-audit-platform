from abc import ABC, abstractmethod

from database.core.context.context_builder import AuditContextBuilder


class BaseAudit(ABC):

    code = ""
    name = ""

    def __init__(self):

        self.context_builder = AuditContextBuilder()

    @abstractmethod
    def analyze(self):
        pass

    def run(self):

        return {
            "audit": self.name,
            "result": self.analyze(),
        }

    def build_context(self, order):

        return self.context_builder.build(order)
