import argparse

from commands.status import run as status
from commands.scan import run as scan

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

else:
    print("Unknown command")