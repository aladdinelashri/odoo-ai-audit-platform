from dataclasses import dataclass
from typing import Any


@dataclass
class ClientProfile:

    organization_resolver: str

    organization_config: dict[str, Any]
