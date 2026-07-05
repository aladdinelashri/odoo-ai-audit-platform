from knowledge.builders.knowledge_builder import KnowledgeBuilder
from knowledge.exporters.knowledge_exporter import KnowledgeExporter


def run():

    print()
    print("=== Knowledge Builder ===")
    print()

    builder = KnowledgeBuilder()
    exporter = KnowledgeExporter()

    knowledge = builder.build()

    exporter.export(knowledge)

    print()
    print("===================================")
    print(" Knowledge Build Completed")
    print("===================================")
