"""
Architecture V3

Core Pipeline End-to-End Test
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))

from database.core.pipeline.pipeline import Pipeline

TEST_QUERIES = [

    "show invoices",

    "show posted invoices",

    "show posted invoices greater than 1000",

    "show invoices less than 500",

    "count invoices",

    "sum invoices",

    "average invoice amount",

]


def main():

    pipeline = Pipeline()

    print()

    print("=" * 80)

    print("CORE PIPELINE TEST")

    print("=" * 80)

    print()

    for query in TEST_QUERIES:

        print("=" * 80)

        print(query)

        print("-" * 80)

        try:

            result = pipeline.execute(query)

            print(result.to_dict())

        except Exception as exc:

            print(exc)

        print()


if __name__ == "__main__":

    main()
