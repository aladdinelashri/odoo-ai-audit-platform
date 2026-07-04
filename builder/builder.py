import argparse

from commands.status import run as status


parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="Command to execute"
)

args = parser.parse_args()


if args.command == "status":
    status()

else:
    print("Unknown command")