from database.core.profile import ProfileLoader

from .object_traverser import ObjectTraverser


class BusinessUnitEngine:

    def __init__(self):

        self.profile = ProfileLoader().load()
        self.traverser = ObjectTraverser()

    def resolve(self, order):

        config = self.profile.organization_config

        return self.traverser.traverse(
            start_model="pos.order",
            start_record=order,
            path=config["path"],
        )
