from pathlib import Path
from commands.inspect import run as inspect

ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "database" / "exports" / "raw"


def run():
    files = sorted(EXPORTS.glob("*.xlsx"))

    if not files:
        print("No Excel files found.")
        return

    print(f"\nFound {len(files)} Excel files\n")

    for file in files:
        model = file.stem
        print(f"Building: {model}")
        inspect(model)

    print("\nBuild completed successfully.")