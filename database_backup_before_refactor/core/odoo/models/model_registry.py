from .pos_models import POSModels
from .accounting_models import AccountingModels


class OdooModelRegistry:

    def __init__(self):
        self.models = {
            "pos": POSModels(),
            "accounting": AccountingModels(),
        }

    def get(self, name):
        return self.models[name]
