from pathlib import Path

RAW_EXPORT_PATH = Path(__file__).resolve().parents[2] / "database" / "exports" / "raw"


def run():
    print("=" * 50)
    print("Odoo AI Audit Platform")
    print("Metadata Scan")
    print("=" * 50)

    if not RAW_EXPORT_PATH.exists():
        print(f"Folder not found: {RAW_EXPORT_PATH}")
        return

    files = sorted(RAW_EXPORT_PATH.glob("*.xlsx"))

    if not files:
        print("No Excel files found.")
        return

    print(f"\nFound {len(files)} exported models:\n")

    for file in files:
        print(f"✓ {file.stem}")

    print("\nScan completed successfully.")