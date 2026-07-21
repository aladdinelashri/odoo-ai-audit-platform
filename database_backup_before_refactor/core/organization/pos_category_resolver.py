from .business_unit import BusinessUnit
from .resolver import BusinessUnitResolver


class CategoryBusinessUnitResolver(BusinessUnitResolver):
    """
    Resolve Business Unit from POS Category.
    """

    SOURCE = "pos.category"

    def resolve(self, record):

        category = record.get("category_id")

        if not category:
            return BusinessUnit(
                id=None,
                code=None,
                name="Unknown",
                source=self.SOURCE,
            )

        return BusinessUnit(
            id=category[0],
            code=str(category[0]),
            name=category[1],
            source=self.SOURCE,
        )
