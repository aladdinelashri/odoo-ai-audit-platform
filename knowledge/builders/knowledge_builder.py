import json
from pathlib import Path

from knowledge.pipeline.default_pipeline import create_pipeline


class KnowledgeBuilder:

    def __init__(self):

        self.metadata_file = Path(
            "data/metadata/database.json"
        )

    def build(self):

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8"
        ) as f:

            metadata = json.load(f)

        pipeline = create_pipeline()

        knowledge = {}

        for table_name, table_data in metadata.items():

            knowledge[table_name] = pipeline.run(
                table_name,
                table_data
            )

        return knowledge
