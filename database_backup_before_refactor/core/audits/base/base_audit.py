from abc import ABC, abstractmethod


class BaseAudit(ABC):
    """
    Base class for every audit module.
    """

    name = "Base Audit"

    @abstractmethod
    def analyze(self):
        """
        Execute the audit.
        """
        raise NotImplementedError

    def run(self):
        return {
            "audit": self.name,
            "result": self.analyze(),
        }
