import argparse

from pm.account import delete_account, view_account_history, update_account, \
    copy_account_credentials, view_account_credentials, create_account, \
    list_accounts
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
    description = "Create a new database for storing passwords."
    setup_program_parser = program_subparser.add_parser("setup", description=description, help=description.lower())
    setup_program_parser.add_argument("--db", type=str, help="name of the database to create", required=True)
    setup_program_parser.set_defaults(func=setup_safe)


def attach_store_subparser(program_subparser):
    description = "Create and manage a password stores."
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
    description = "Create and manage password in a store."
    account_program_parser = program_subparser.add_parser("account", description=description, help=description.lower())
    account_command_subparser = account_program_parser.add_subparsers(dest="command", title="command", metavar="<command>")

    list_accounts_parser = account_command_subparser.add_parser("list", help="List accounts")
    list_accounts_parser.add_argument("--db", required=True, help="Database name")
    list_accounts_parser.add_argument("--store", required=True, help="Store name")
    list_accounts_parser.set_defaults(func=list_accounts)

    create_account_parser = account_command_subparser.add_parser("create", help="Create an account")
    create_account_parser.add_argument("--db", required=True, help="Database name")
    create_account_parser.add_argument("--store", required=True, help="Store name")
    create_account_parser.add_argument("--account", required=True, help="Account name")
    create_account_parser.add_argument("--username", help="Username")
    create_account_parser.add_argument("--email", help="Email")
    create_account_password_group = create_account_parser.add_mutually_exclusive_group(required=True)
    create_account_password_group.add_argument("--password", action="store_true", help="Password to use")
    create_account_password_group.add_argument("--auto-gen-password", action="store_true", help="Auto-generate password")
    create_account_parser.add_argument("--pass-min-length", type=int, help="Minimum password length")
    create_account_parser.add_argument("--pass-max-length", type=int, help="Maximum password length")
    create_account_parser.add_argument("--pass-no-special", action="store_true", help="Exclude special characters")
    create_account_parser.add_argument("--pass-no-digits", action="store_true", help="Exclude digits")
    create_account_parser.add_argument("--pass-exclude-chars", help="Characters to exclude from password")
    create_account_parser.set_defaults(func=create_account)

    view_account_parser = account_command_subparser.add_parser("view", help="View an account")
    view_account_parser.add_argument("--db", required=True, elp="Database name")
    view_account_parser.add_argument("--store", required=True, help="Store name")
    view_account_parser.add_argument("--account", required=True, help="Account name")
    view_account_parser.add_argument( "--type", nargs="+", choices=["email", "username", "password", "all"], required=True, help="Choose what to view: email, username, password, or all")
    view_account_parser.set_defaults(func=view_account_credentials)

    copy_account_parser = account_command_subparser.add_parser("copy", help="Copy an account")
    copy_account_parser.add_argument("--db", required=True, help="Database name")
    copy_account_parser.add_argument("--store", required=True, help="Store name")
    copy_account_parser.add_argument("--account", required=True, help="Account name")
    copy_account_parser.add_argument("--type", choices=["username", "email", "password"], required=True, help="Choose what to copy: username, email or password")
    copy_account_parser.set_defaults(func=copy_account_credentials)

    update_account_parser = account_command_subparser.add_parser("update", help="Update an account")
    update_account_parser.add_argument("--db", required=True, help="Database name")
    update_account_parser.add_argument("--store", required=True, help="Store name")
    update_account_parser.add_argument("--account", required=True, help="Account name")
    update_account_password_group = update_account_parser.add_mutually_exclusive_group(required=True)
    update_account_password_group.add_argument("--password", action="store_true", help="Use own password")
    update_account_password_group.add_argument("--auto-gen-password", action="store_true", help="Auto-generate password")
    update_account_parser.add_argument("--pass-min-length", type=int, help="Minimum password length")
    update_account_parser.add_argument("--pass-max-length", type=int, help="Maximum password length")
    update_account_parser.add_argument("--pass-no-special", action="store_true", help="Exclude special characters")
    update_account_parser.add_argument("--pass-no-digits", action="store_true", help="Exclude digits")
    update_account_parser.add_argument("--pass-exclude-chars", help="Characters to exclude from password")
    update_account_parser.set_defaults(func=update_account)

    delete_account_parser = account_command_subparser.add_parser("delete", help="Delete an account")
    delete_account_parser.add_argument("--db", required=True, help="Database name")
    delete_account_parser.add_argument("--store", required=True, help="Store name")
    delete_account_parser.add_argument("--account", required=True, help="Account name")
    delete_account_parser.set_defaults(func=delete_account)

    history_account_parser = account_command_subparser.add_parser("history", help="View account history")
    history_account_parser.add_argument("--db", required=True, help="Database name")
    history_account_parser.add_argument("--store", required=True, help="Store name")
    history_account_parser.add_argument("--account", required=True, help="Account name")
    history_account_parser.set_defaults(func=view_account_history)
