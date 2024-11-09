import argparse


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        print(0.1)
        return 0


def create_parser():
    parser = argparse.ArgumentParser(description="Safe Password Manager")
    parser.add_argument("-v", "--version", action="store_true", help="print version")

    return parser


'''
def create_parser():
    parser = argparse.ArgumentParser(description="Safe Password Manager")
    parser.add_argument("-v", "--version", action="store_true", help="print version")
    program_subparser = parser.add_subparsers(dest="program", title="program", metavar="<program>", required=True)

    # Attach program subparsers
    attach_setup_subparser(program_subparser)
    attach_store_subparser(program_subparser)
    attach_account_subparser(program_subparser)

    return parser


def attach_setup_subparser(program_subparser):
    setup_program_parser = program_subparser.add_parser("setup", help="Create a new database for storing passwords")
    setup_program_parser.add_argument("--db", type=str, help="name of the database to create", required=True)
    setup_program_parser.set_defaults(func=setup_safe)


def setup_safe(args):
    pass


def attach_store_subparser(program_subparser):
    store_program_subparser = program_subparser.add_parser("store", help="Create and manage a password stores")
    store_command_subparser = store_program_subparser.add_subparsers(
        dest="command", title="commands", metavar="<command>", required=True)

    # Create subparser
    create_store_password = store_command_subparser.add_parser("create", help="Create a new store")
    create_store_password.add_argument("--db", required=True, help="Name of the database")
    create_store_password.add_argument("--store", required=True, help="Name of the store")


    # Rename subparser
    rename_store_parser = store_command_subparser.add_parser("rename", help="Rename a store")
    rename_store_parser.add_argument("--db", required=True, help="Name of the database")
    rename_store_parser.add_argument("--oldname", required=True, help="Old name of the store")
    rename_store_parser.add_argument("--newname", required=True, help="New name of the store")

    # Delete subparser
    delete__store_parser = store_command_subparser.add_parser("delete", help="Delete a store")
    delete__store_parser.add_argument("--db", required=True, help="Name of the database")
    delete__store_parser.add_argument("--name", required=True, help="Name of the store")

    # List subparser
    list_store_parser = store_command_subparser.add_parser("list", help="List all stores")
    list_store_parser.add_argument("--db", required=True, help="Name of the database")
    list_store_parser.set_defaults(func=execute_store_program)


def execute_store_program(args):
    pass


def attach_account_subparser(program_subparser):
    account_program_parser = program_subparser.add_parser("account", help="Account subcommand")
    account_command_subparser = account_program_parser.add_subparsers(dest="command", title="command", metavar="<command>")

    # List subparser
    list_accounts_parser = account_command_subparser.add_parser("list", help="List accounts")
    list_accounts_parser.add_argument("--db", required=True, help="Database name")
    list_accounts_parser.add_argument("--store", required=True, help="Store name")

    # Create subparser
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

    # View subparser
    view_account_parser = account_command_subparser.add_parser("view", help="View an account")
    view_account_parser.add_argument("--db", required=True, help="Database name")
    view_account_parser.add_argument("--store", required=True, help="Store name")
    view_account_parser.add_argument("--account", required=True, help="Account name")
    view_account_parser.add_argument(
        "--type", nargs="+",
        choices=["email", "username", "password", "all"],
        required=True,
        help="Choose what to view: email, username, password, or all")

    # Copy subparser
    copy_account_parser = account_command_subparser.add_parser("copy", help="Copy an account")
    copy_account_parser.add_argument("--db", required=True, help="Database name")
    copy_account_parser.add_argument("--store", required=True, help="Store name")
    copy_account_parser.add_argument("--account", required=True, help="Account name")
    copy_account_parser.add_argument(
        "--type", choices=["username", "email", "password"],
        required=True, help="Choose what to copy: username, email or password")

    # Update subparser
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

    # Delete subparser
    delete_account_parser = account_command_subparser.add_parser("delete", help="Delete an account")
    delete_account_parser.add_argument("--db", required=True, help="Database name")
    delete_account_parser.add_argument("--store", required=True, help="Store name")
    delete_account_parser.add_argument("--account", required=True, help="Account name")

    # History subparser
    history_account_parser = account_command_subparser.add_parser("history", help="View account history")
    history_account_parser.add_argument("--db", required=True, help="Database name")
    history_account_parser.add_argument("--store", required=True, help="Store name")
    history_account_parser.add_argument("--account", required=True, help="Account name")
'''

# Starting point
if __name__ == "__main__":
    main()
