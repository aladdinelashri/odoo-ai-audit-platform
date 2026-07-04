from pathlib import Path
from datetime import datetime
import json

from commands.inspect import run as inspect

ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "database" / "exports" / "raw"
METADATA = ROOT / "database" / "metadata"


def run():

    files = sorted(EXPORTS.glob("*.xlsx"))

    if not files:
        print("No Excel files found.")
        return

    index = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "models": []
    }

    print(f"\nFound {len(files)} Excel files\n")

    for file in files:

        model = file.stem

        print(f"Building: {model}")

        inspect(model)

        metadata_file = METADATA / f"{model}.json"

        if metadata_file.exists():

            with open(metadata_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            index["models"].append({
                "model": data["model"],
                "rows": data["rows"],
                "columns": data["columns"],
                "file": metadata_file.name
            })

    with open(METADATA / "models.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4, ensure_ascii=False)

    print("\nmodels.json generated successfully.")