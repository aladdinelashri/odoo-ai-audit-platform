import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from commands.status import run as status
from commands.scan import run as scan
from commands.models import run as models
from commands.inspect import run as inspect
from commands.build import run as build
from commands.dictionary import run as dictionary
from commands.report import run as report
from commands.relations import run as relations
from commands.discover_schema import run as discover_schema
from commands.metadata import run as metadata
from commands.knowledge import run as knowledge
from commands.audit import run as audit
from commands.audit_ai import run as audit_ai
from commands.sql import run as sql
from commands.rules import run as rules
from commands.connect import run as connect
from commands.executive import run as executive

parser = argparse.ArgumentParser(
    description="Odoo AI Audit Platform Builder"
)

parser.add_argument(
    "command",
    help="Command to execute"
)

parser.add_argument(
    "model",
    nargs="?",
    default=None,
    help="Odoo model name"
)

args = parser.parse_args()

if args.command == "status":
    status()

elif args.command == "scan":
    scan()

elif args.command == "models":
    models()

elif args.command == "inspect":
    inspect(args.model)

elif args.command == "build":
    build()

elif args.command == "dictionary":
    dictionary()

elif args.command == "report":
    report()

elif args.command == "relations":
    relations()

elif args.command == "discover-schema":
    discover_schema()

elif args.command == "metadata":
    metadata()

elif args.command == "knowledge":
    knowledge()

elif args.command == "audit":
    audit()

elif args.command == "audit-ai":
    audit_ai()

elif args.command == "sql":
    sql()

elif args.command == "rules":
    rules()

elif args.command == "connect":
    connect()

elif args.command == "executive":
    executive()

else:
    print(f"Unknown command: {args.command}")
