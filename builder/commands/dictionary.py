from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

METADATA = ROOT / "database" / "metadata"
KNOWLEDGE = ROOT / "database" / "knowledge"


def run():

    KNOWLEDGE.mkdir(parents=True, exist_ok=True)

    dictionary = {
        "version": "1.0",
        "models": []
    }

    for file in sorted(METADATA.glob("*.json")):

        if file.name == "models.json":
            continue

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        dictionary["models"].append({
            "model": data["model"],
            "rows": data["rows"],
            "columns": data["columns"],
            "fields": data["fields"]
        })

    output = KNOWLEDGE / "data_dictionary.json"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=4, ensure_ascii=False)

    print(f"\nData Dictionary generated:\n{output}")