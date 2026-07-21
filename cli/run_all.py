import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from database.core.audits.runner.audit_runner import AuditRunner


def main():

    runner = AuditRunner()

    results = runner.run_all()

    pprint(results)


if __name__ == "__main__":
    main()
