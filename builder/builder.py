import argparse

from commands.status import run as status
from commands.scan import run as scan
from commands.models import run as models
from commands.inspect import run as inspect

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
    if args.model is None:
        print("Please specify the Odoo model.")
    else:
        inspect(args.model)

else:
    print(f"Unknown command: {args.command}")