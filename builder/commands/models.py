from pathlib import Path
import yaml

CONFIG = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "config"
    / "models.yaml"
)

def run():
    with open(CONFIG, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    print("\nRegistered Odoo Models\n")

    for module, models in data["modules"].items():
        print(f"[{module}]")
        for model in models:
            print(f"  - {model}")
        print()