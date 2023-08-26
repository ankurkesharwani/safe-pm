import sys
import argparse

from manager.account_manager import AccountManager


def parse_arguments():
    # Create the main argument parser
    parser = argparse.ArgumentParser(description="Account Management Program")

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="<command>")

    # List subparser
    list_parser = subparsers.add_parser("list", help="List accounts")
    list_parser.add_argument("--db", required=True, help="Database name")
    list_parser.add_argument("--store", required=True, help="Store name")

    # Create subparser
    create_parser = subparsers.add_parser("create", help="Create an account")
    create_parser.add_argument("--db", required=True, help="Database name")
    create_parser.add_argument("--store", required=True, help="Store name")
    create_parser.add_argument("--name", required=True, help="Account name")
    create_parser.add_argument("--username", help="Username")
    create_parser.add_argument("--email", help="Email")
    password_group = create_parser.add_mutually_exclusive_group(required=True)
    password_group.add_argument("--password", help="Password to use")
    password_group.add_argument("--auto-gen-password", action="store_true", help="Auto-generate password")
    create_parser.add_argument("--pass-min-length", type=int, help="Minimum password length")
    create_parser.add_argument("--pass-max-length", type=int, help="Maximum password length")
    create_parser.add_argument("--pass-no-special", action="store_true", help="Exclude special characters")
    create_parser.add_argument("--pass-no-digits", action="store_true", help="Exclude digits")
    create_parser.add_argument("--pass-exclude-chars", help="Characters to exclude from password")

    # View subparser
    view_parser = subparsers.add_parser("view", help="View an account")
    view_parser.add_argument("--db", required=True, help="Database name")
    view_parser.add_argument("--store", required=True, help="Store name")
    view_parser.add_argument("--name", required=True, help="Account name")
    view_parser.add_argument(
        "--type", nargs="+", 
        choices=["email", "username", "password", "all"],
        required=True,
        help="Choose what to view: email, username, password, or all")

    # Copy subparser
    copy_parser = subparsers.add_parser("copy", help="Copy an account")
    copy_parser.add_argument("--db", required=True, help="Database name")
    copy_parser.add_argument("--store", required=True, help="Store name")
    copy_parser.add_argument("--name", required=True, help="Account name")
    copy_parser.add_argument(
        "--type", choices=["username", "email", "password"], 
        required=True, help="Choose what to copy: username, email or password")

    # Update subparser
    update_parser = subparsers.add_parser("update", help="Update an account")
    update_parser.add_argument("--db", required=True, help="Database name")
    update_parser.add_argument("--store", required=True, help="Store name")
    update_parser.add_argument("--name", required=True, help="Account name")
    password_group = update_parser.add_mutually_exclusive_group(required=True)
    password_group.add_argument("--password", help="Password to use")
    password_group.add_argument("--auto-gen-password", action="store_true", help="Auto-generate password")
    update_parser.add_argument("--pass-min-length", type=int, help="Minimum password length")
    update_parser.add_argument("--pass-max-length", type=int, help="Maximum password length")
    update_parser.add_argument("--pass-no-special", action="store_true", help="Exclude special characters")
    update_parser.add_argument("--pass-no-digits", action="store_true", help="Exclude digits")
    update_parser.add_argument("--pass-exclude-chars", help="Characters to exclude from password")

    # Delete subparser
    delete_parser = subparsers.add_parser("delete", help="Delete an account")
    delete_parser.add_argument("--db", required=True, help="Database name")
    delete_parser.add_argument("--store", required=True, help="Store name")
    delete_parser.add_argument("--name", required=True, help="Account name")

    # History subparser
    history_parser = subparsers.add_parser("history", help="View account history")
    history_parser.add_argument("--db", required=True, help="Database name")
    history_parser.add_argument("--store", required=True, help="Store name")
    history_parser.add_argument("--name", required=True, help="Account name")

    # Parse the command-line arguments
    args = parser.parse_args()

    if not args.command in ["list", "create", "view", "copy", "update", "delete", "history"]:
        print("error: A valid command is missing")
        parser.print_help()
        sys.exit(1)

    return args


def main():
    args = parse_arguments()

    account_manager = AccountManager()

    if args.command == "list":
        account_manager.list_accounts(args.db, args.store)
    elif args.command == "create":
        account_manager.create_account(
            args.db,
            args.store,
            args.name,
            args.username,
            args.email,
            args.password,
            args.auto_gen_password,
            args.pass_min_length,
            args.pass_max_length,
            args.pass_no_special,
            args.pass_no_digits,
            args.pass_exclude_chars)
    elif args.command == "view":
        account_manager.view_account(
            args.db,
            args.store,
            args.name,
            args.type)
    elif args.command == "copy":
        account_manager.copy_account(
            args.db,
            args.store,
            args.name,
            args.type)
    elif args.command == "update":
        account_manager.update_account(
            args.db,
            args.store,
            args.name,
            args.auto_gen_password,
            args.pass_min_length,
            args.pass_max_length,
            args.pass_no_special,
            args.pass_no_digits,
            args.pass_exclude_chars)
    elif args.command == "delete":
        account_manager.delete_account(args.db, args.store, args.name)
    elif args.command == "history":
        account_manager.account_history(args.db, args.store, args.name)
    else:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)
