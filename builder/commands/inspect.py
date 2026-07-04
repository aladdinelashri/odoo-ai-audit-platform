from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

EXPORTS = ROOT / "database" / "exports" / "raw"
METADATA = ROOT / "database" / "metadata"


def run(model_name):

    excel_file = EXPORTS / f"{model_name}.xlsx"

    if not excel_file.exists():
        print(f"Model file not found:\n{excel_file}")
        return

    df = pd.read_excel(excel_file)

    fields = []

    for column in df.columns:
        fields.append({
            "name": column,
            "type": str(df[column].dtype)
        })

    metadata = {
        "model": model_name,
        "source": excel_file.name,
        "rows": len(df),
        "columns": len(df.columns),
        "fields": fields
    }

    METADATA.mkdir(parents=True, exist_ok=True)

    output = METADATA / f"{model_name}.json"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"Metadata generated successfully:\n{output}")