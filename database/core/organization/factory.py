from database.core.profile import ProfileLoader

from .pos_category_resolver import CategoryBusinessUnitResolver


class BusinessUnitResolverFactory:

    @staticmethod
    def create():

        profile = ProfileLoader().load()

        if profile.organization_resolver == "pos_category":
            return CategoryBusinessUnitResolver(
                profile.organization_config
            )

        raise ValueError(
            f"Unknown resolver: {profile.organization_resolver}"
        )
