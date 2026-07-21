from .connector import OdooConnector
from .data_adapter import OdooDataAdapter
from .metadata_adapter import OdooMetadataAdapter


class OdooRegistry:

    def __init__(self):
        self.services = {
            "connector": OdooConnector(),
            "data": OdooDataAdapter(),
            "metadata": OdooMetadataAdapter(),
        }

    def get(self, name):
        return self.services[name]
