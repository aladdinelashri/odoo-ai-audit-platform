from .config import BUSINESS_UNIT_SOURCE
from .category_resolver import CategoryBusinessUnitResolver


class BusinessUnitResolverFactory:
    """
    Factory for Business Unit Resolvers.
    """

    @staticmethod
    def create(source=None):

        if source is None:
            source = BUSINESS_UNIT_SOURCE

        if source == "pos.category":
            return CategoryBusinessUnitResolver()

        raise ValueError(
            f"Unsupported Business Unit source: {source}"
        )
