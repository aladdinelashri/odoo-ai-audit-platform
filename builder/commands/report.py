from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE = ROOT / "database" / "knowledge" / "data_dictionary.json"


def run():

    if not KNOWLEDGE.exists():
        print("Data Dictionary not found.")
        return

    with open(KNOWLEDGE, "r", encoding="utf-8") as f:
        data = json.load(f)

    models = len(data["models"])
    total_rows = sum(m["rows"] for m in data["models"])
    total_fields = sum(len(m["fields"]) for m in data["models"])

    print("\n======================================")
    print(" Odoo AI Audit Platform Report")
    print("======================================")
    print(f"Models       : {models}")
    print(f"Rows         : {total_rows:,}")
    print(f"Fields       : {total_fields}")
    print(f"Version      : {data['version']}")
    print("======================================")