from database.discovery.model_discovery import ModelDiscovery
from database.discovery.relation_discovery import RelationDiscovery
from database.discovery.semantic_discovery import SemanticDiscovery
from database.discovery.statistics import DiscoveryStatistics


class DiscoveryEngine:

    def __init__(self):

        self.models = ModelDiscovery()

        self.relations = RelationDiscovery()

        self.semantic = SemanticDiscovery()

        self.statistics = DiscoveryStatistics()

    # ---------------------------------------------------------

    def discover(self):

        return {

            "models": self.models.discover(),

            "relations": self.relations.discover(),

            "semantic": self.semantic.discover(),

            "statistics": self.statistics.collect()

        }
