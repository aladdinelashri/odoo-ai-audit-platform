from pathlib import Path

from audit.core.metadata_loader import MetadataLoader


class AuditCatalog:

    def __init__(self):

        self.path = Path("audit/metadata/rules")

    def load(self):

        rules = []

        for file in sorted(self.path.glob("*.json")):

            rules.append(
                MetadataLoader.load_json(
                    f"rules/{file.name}"
                )
            )

        return rules

    def count(self):

        return len(self.load())
