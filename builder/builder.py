import argparse

from commands.status import run as status
from commands.scan import run as scan
from commands.models import run as models

parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="Command to execute"
)

args = parser.parse_args()

if args.command == "status":
    status()

elif args.command == "scan":
    scan()

elif args.command == "models":
    models()

else:
    print("Unknown command")