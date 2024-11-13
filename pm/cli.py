import argparse

def cli_start():
    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        print(0.1)
        return 0

    if args.program is not None and hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        return -1


def create_parser():
    parser = argparse.ArgumentParser(prog="safe-pm", description="SafePM: A secure, simple, open-source password manager.")
    parser.add_argument("-v", "--version", action="store_true", help="Print version")
    program_subparser = parser.add_subparsers(dest="program", title="program", metavar="<program>")

    # Attach program subparsers
    attach_setup_subparser(program_subparser)

    return parser


def attach_setup_subparser(program_subparser):
    description = "Create a new database for storing passwords"
    setup_program_parser = program_subparser.add_parser("setup", description=description, help=description.lower())
    setup_program_parser.add_argument("--db", type=str, help="name of the database to create", required=True)
    setup_program_parser.set_defaults(func=setup_safe)


def setup_safe(args):
    print(args)
