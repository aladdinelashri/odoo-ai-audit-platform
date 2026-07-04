from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE = ROOT / "database" / "knowledge"
DICTIONARY = KNOWLEDGE / "data_dictionary.json"


def run():

    if not DICTIONARY.exists():
        print("Data Dictionary not found.")
        return

    with open(DICTIONARY, "r", encoding="utf-8") as f:
        data = json.load(f)

    relations = []

    for model in data["models"]:

        for field in model["fields"]:

            name = field["name"]

            if (
                name.endswith("_id")
                or name.endswith("_ids")
            ):

                relations.append({
                    "model": model["model"],
                    "field": name
                })

    output = KNOWLEDGE / "relationships.json"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=4, ensure_ascii=False)

    print(f"\nRelationships found: {len(relations)}")