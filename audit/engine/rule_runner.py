import importlib
import inspect

from database.sql.executor import SQLExecutor

from audit.catalog.catalog import AuditCatalog
from audit.evidence.collector import EvidenceCollector
from audit.rules.base_rule import AuditRule


class AuditRuleRunner:

    def __init__(self):

        self.executor = SQLExecutor()

        self.collector = EvidenceCollector()

        self.catalog = AuditCatalog()

        self.rules = self.load_rules()

    def load_rules(self):

        loaded_rules = []

        metadata = self.catalog.load()

        for rule in metadata:

            module_name = rule["id"].lower()

            module = importlib.import_module(
                f"audit.rules.{module_name}"
            )

            for _, obj in inspect.getmembers(module):

                if (
                    inspect.isclass(obj)
                    and issubclass(obj, AuditRule)
                    and obj is not AuditRule
                ):

                    loaded_rules.append(obj())

        return loaded_rules

    def run(self):

        for rule in self.rules:

            finding = rule.execute(self.executor)

            self.collector.add(finding)

        return self.collector.summary()
