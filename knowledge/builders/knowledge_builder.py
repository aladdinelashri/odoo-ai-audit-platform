import json
from pathlib import Path

from knowledge.builders.domain_builder import DomainBuilder


class KnowledgeBuilder:

    def __init__(self):

        self.metadata_file = Path("data/metadata/database.json")

        self.domain_builder = DomainBuilder()

    def build(self):

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8"
        ) as f:

            metadata = json.load(f)

        knowledge = {}

        for table_name, table_data in metadata.items():

            knowledge[table_name] = {

                **table_data,

                "domain": self.domain_builder.classify(table_name)

            }

        return knowledge
