import argparse

from pm.setup import setup_safe
from pm.store import create_store_password, rename_store, delete_store, list_stores


def cli_start():
    print_stacktrace = False

    try:
        parser = create_parser()
        args = parser.parse_args()
        print_stacktrace = args.stacktrace

        if args.version:
            print(0.1)
            return

        if args.command is not None and hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
    except Exception as catch_all_exception:
        if print_stacktrace:
            raise catch_all_exception
        else:
            print(f"Encountered error: {catch_all_exception}")


def create_parser():
    parser = argparse.ArgumentParser(prog="safe-pm", description="SafePM: A secure, simple, open-source password manager.")
    parser.add_argument("-v", "--version", action="store_true", help="Print version")
    parser.add_argument("-s", "--stacktrace", action="store_true", required=False, help="Prints stack trace in case of error for debugging",)
    program_subparser = parser.add_subparsers(dest="program", title="program", metavar="<program>")

    attach_setup_subparser(program_subparser)
    attach_store_subparser(program_subparser)
    attach_account_subparser(program_subparser)

    return parser


def attach_setup_subparser(program_subparser):
    description = "Create a new database for storing passwords"
    setup_program_parser = program_subparser.add_parser("setup", description=description, help=description.lower())
    setup_program_parser.add_argument("--db", type=str, help="name of the database to create", required=True)
    setup_program_parser.set_defaults(func=setup_safe)


def attach_store_subparser(program_subparser):
    description = "Create and manage a password stores"
    store_program_parser = program_subparser.add_parser("store", description=description, help=description.lower())
    store_command_parser = store_program_parser.add_subparsers(dest="command", title="commands", metavar="<command>", required=True)

    create_store_password_parser = store_command_parser.add_parser("create", help="Create a new store")
    create_store_password_parser.add_argument("--db", required=True, help="Name of the database")
    create_store_password_parser.add_argument("--store", required=True, help="Name of the store")
    create_store_password_parser.set_defaults(func=create_store_password)

    rename_store_parser = store_command_parser.add_parser("rename", help="Rename a store")
    rename_store_parser.add_argument("--db", required=True, help="Name of the database")
    rename_store_parser.add_argument("--store", required=True, help="Store to rename")
    rename_store_parser.add_argument("--new-name", required=True, help="New name of the store")
    rename_store_parser.set_defaults(func=rename_store)

    delete_store_parser = store_command_parser.add_parser("delete", help="Delete a store")
    delete_store_parser.add_argument("--db", required=True, help="Name of the database")
    delete_store_parser.add_argument("--name", required=True, help="Name of the store")
    delete_store_parser.set_defaults(func=delete_store)

    list_stores_parser = store_command_parser.add_parser("list", help="List all stores")
    list_stores_parser.add_argument("--db", required=True, help="Name of the database")
    list_stores_parser.set_defaults(func=list_stores)


def attach_account_subparser(program_subparser):
    pass
