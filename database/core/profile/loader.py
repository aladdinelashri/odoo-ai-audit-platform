from pathlib import Path

import yaml

from .profile import ClientProfile


class ProfileLoader:

    def __init__(self):

        self.profile_path = (
            Path(__file__).resolve().parents[3]
            / "config"
            / "client"
            / "organization.yaml"
        )

    def load(self):

        with open(self.profile_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        resolver = data["organization"]["resolver"]

        return ClientProfile(
            organization_resolver=resolver,
            organization_config=data["resolvers"][resolver],
        )
