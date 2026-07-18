from .security_engine import SecurityEngine
from .access_control import AccessControl


class SecurityRegistry:

    def __init__(self):
        self.services = {
            "engine": SecurityEngine(),
            "access": AccessControl(),
        }

    def get(self, name):
        return self.services[name]
