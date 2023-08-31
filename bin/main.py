import argparse
import store
import account
import setup


def create_parser():
    parser = argparse.ArgumentParser(description="Safe Password Manager")
    parser.add_argument("-v", "--version", action="store_true", help="print version")
    program_subparser = parser.add_subparsers(dest="program", title="program", metavar="<program>", required=True)
    setup.attach_subparser(program_subparser)
    account.attach_subparser(program_subparser)
    store.attach_subparser(program_subparser)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.version:
        print(0.1)
        return 0

    if args.program == "setup":
        return setup.execute(args)
    elif args.program == "account":
        return account.execute(args)
    elif args.program == "store":
        return store.execute(args)
    else:
        return 1


if __name__ == "__main__":
    main()
