import json
from pathlib import Path

from knowledge.builders.domain_builder import DomainBuilder
from knowledge.builders.risk_builder import RiskBuilder
from knowledge.builders.audit_builder import AuditBuilder


class KnowledgeBuilder:

    def __init__(self):

        self.metadata_file = Path("data/metadata/database.json")

        self.domain_builder = DomainBuilder()
        self.risk_builder = RiskBuilder()
        self.audit_builder = AuditBuilder()

    def build(self):

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8"
        ) as f:

            metadata = json.load(f)

        knowledge = {}

        for table_name, table_data in metadata.items():

            risk = self.risk_builder.classify(table_name)

            knowledge[table_name] = {

                **table_data,

                "domain": self.domain_builder.classify(table_name),

                "risk": risk,

                "audit_tests": self.audit_builder.build(risk)

            }

        return knowledge
