from database.core.profile import ProfileLoader

from database.core.organization.entity import BusinessUnit
from .business_unit_engine import BusinessUnitEngine
from .business_unit_mapper import BusinessUnitMapper


class BusinessUnitService:

    def __init__(self):

        self.profile = ProfileLoader().load()
        self.engine = BusinessUnitEngine()
        self.mapper = BusinessUnitMapper()

    def resolve(self, order) -> BusinessUnit | None:

        record = self.engine.resolve(order)

        return self.mapper.map(
            record,
            self.profile.organization_config["model"],
        )
