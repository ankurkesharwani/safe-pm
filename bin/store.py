import sys
import argparse

from manager.store_manager import StoreManager


def parse_arguments():
    # Create the main argument parser
    parser = argparse.ArgumentParser(
        prog="safe-pm store", description="Create and manage a password stores")

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")

    # Create subparser
    create_parser = subparsers.add_parser("create", help="Create a new store")
    create_parser.add_argument("--db", required=True, help="Name of the database")
    create_parser.add_argument("--name", required=True, help="Name of the store")

    # Rename subparser
    rename_parser = subparsers.add_parser("rename", help="Rename a store")
    rename_parser.add_argument("--db", required=True, help="Name of the database")
    rename_parser.add_argument("--oldname", required=True, help="Old name of the store")
    rename_parser.add_argument("--newname", required=True, help="New name of the store")

    # Delete subparser
    delete_parser = subparsers.add_parser("delete", help="Delete a store")
    delete_parser.add_argument("--db", required=True, help="Name of the database")
    delete_parser.add_argument("--name", required=True, help="Name of the store")

    # List subparser
    list_parser = subparsers.add_parser("list", help="List all stores")
    list_parser.add_argument("--db", required=True, help="Name of the database")

    # Parse the command-line arguments
    args = parser.parse_args()

    if not args.command in ["create", "rename", "delete", "list"]:
        print("error: A valid command is missing")
        parser.print_help()
        sys.exit(1)

    return args


def main():
    args = parse_arguments()
    store_manager = StoreManager()

    if args.command == "create":
        store_manager.create_store(args.name)
    elif args.command == "rename":
        store_manager.rename_store(args.oldname, args.newname)
    elif args.command == "delete":
        store_manager.delete_store(args.name)
    elif args.command == "list":
        store_manager.list_stores()
    else:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)
