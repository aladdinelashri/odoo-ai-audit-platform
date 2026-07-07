import json
from pathlib import Path

from database.schema.schema_cache import SchemaCache


def build():

    cache = SchemaCache()

    schema = cache.load()

    output = Path("database/schema/schema.json")

    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(
            schema,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"Schema saved to {output}")


if __name__ == "__main__":
    build()
