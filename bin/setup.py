import os
import sys
import argparse

from manager.setup_manager import SetupManager


def get_db_path() -> str:
    script_path = sys.argv
    path_components = script_path[0].split(os.path.sep)[:-2]
    path_components.append("db")
    return os.path.sep.join(path_components)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="safe-pm setup", description="Create a new database for storing passwords")

    parser.add_argument(
        "-n", "--name", type=str, help="name of the database to create", required=True)

    return parser.parse_args()


def main():
    args = parse_arguments()
    name = args.name

    setup = SetupManager()
    return_value = setup.do_setup(get_db_path(), name)

    sys.exit(return_value)


if __name__ == "__main__":
    main()
    sys.exit(0)
