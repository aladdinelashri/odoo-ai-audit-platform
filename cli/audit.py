import sys
from pathlib import Path
from pprint import pprint
import argparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from database.core.audits.runner.audit_runner import AuditRunner


def main():

    parser = argparse.ArgumentParser(
        description="Odoo AI Audit Platform"
    )

    parser.add_argument(
        "audit",
        help="Audit code",
    )

    args = parser.parse_args()

    runner = AuditRunner()

    result = runner.run(args.audit)

    pprint(result)


if __name__ == "__main__":
    main()
