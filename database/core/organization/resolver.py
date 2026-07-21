from abc import ABC, abstractmethod

from .entity import BusinessUnit


class BusinessUnitResolver(ABC):
    """
    Base resolver for Business Units.
    """

    @abstractmethod
    def resolve(self, record):
        """
        Resolve a BusinessUnit from an Odoo record.
        """
        raise NotImplementedError
