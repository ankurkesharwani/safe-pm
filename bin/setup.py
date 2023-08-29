import os
import sys
import argparse

from manager.setup_manager import SetupManager
from common import get_db_path


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="safe-pm setup", description="Create a new database for storing passwords")

    parser.add_argument("--db", type=str, help="name of the database to create", required=True)

    return parser.parse_args()


def main():
    args = parse_arguments()
    db_name = args.db

    setup = SetupManager()
    return_value = setup.do_setup(get_db_path(), db_name)

    sys.exit(return_value)


if __name__ == "__main__":
    main()
    sys.exit(0)
