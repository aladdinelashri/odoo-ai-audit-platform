import json
from pathlib import Path


class MetadataExporter:

    def export(self, data, output_path):
        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return path
