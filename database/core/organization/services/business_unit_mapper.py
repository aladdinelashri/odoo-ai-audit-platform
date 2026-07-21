from database.core.organization.entity import BusinessUnit


class BusinessUnitMapper:

    def map(self, record, model):

        if record is None:
            return None

        return BusinessUnit(
            id=record["id"],
            code=str(record["id"]),
            name=record.get("display_name")
            or record.get("name")
            or str(record["id"]),
            source=model,
        )
