from managers.utils.path_utils import get_db_path
from managers.store_manager import StoreManager


def attach_subparser(program_subparser):
    store_program_subparser = program_subparser.add_parser("store", help="Create and manage a password stores")
    store_command_subparser = store_program_subparser.add_subparsers(
        dest="command", title="commands", metavar="<command>", required=True)

    # Create subparser
    create_parser = store_command_subparser.add_parser("create", help="Create a new store")
    create_parser.add_argument("--db", required=True, help="Name of the database")
    create_parser.add_argument("--store", required=True, help="Name of the store")

    # Rename subparser
    rename_parser = store_command_subparser.add_parser("rename", help="Rename a store")
    rename_parser.add_argument("--db", required=True, help="Name of the database")
    rename_parser.add_argument("--oldname", required=True, help="Old name of the store")
    rename_parser.add_argument("--newname", required=True, help="New name of the store")

    # Delete subparser
    delete_parser = store_command_subparser.add_parser("delete", help="Delete a store")
    delete_parser.add_argument("--db", required=True, help="Name of the database")
    delete_parser.add_argument("--name", required=True, help="Name of the store")

    # List subparser
    list_parser = store_command_subparser.add_parser("list", help="List all stores")
    list_parser.add_argument("--db", required=True, help="Name of the database")


def execute(args):
    store_manager = StoreManager(get_db_path(), args.db)

    if args.command == "create":
        store_manager.create_store(args.store)
    elif args.command == "rename":
        store_manager.rename_store(args.oldname, args.newname)
    elif args.command == "delete":
        store_manager.delete_store(args.store)
    elif args.command == "list":
        store_manager.list_stores()
    else:
        return 1

    return 0
