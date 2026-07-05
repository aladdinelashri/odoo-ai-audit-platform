from database.metadata.builder import MetadataBuilder
from database.metadata.exporter import MetadataExporter


def run():

    print()
    print("=== Metadata Builder ===")
    print()

    builder = MetadataBuilder()
    exporter = MetadataExporter()

    metadata = builder.build()

    exporter.export(metadata)

    print()
    print("===================================")
    print(" Metadata Build Completed")
    print("===================================")
