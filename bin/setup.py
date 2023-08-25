import sqlite3
import os
import sys
import argparse

class Setup:
    def __init__(self, name):
        self.name = name


    def do_setup(self):
        if self.db_exists(self.get_db_path(), self.name):
            print("Database already exists")
            return 1

        self.create_db(self.get_db_path(), self.name)

        if self.db_exists(self.get_db_path(), self.name):
            print("Database created successfully")
            return 0

        else:
            print("Error: Failed to create database")
            return 2


    def get_db_path(self) -> str:
        script_path = sys.argv
        path_components = script_path[0].split(os.path.sep)[:-2]
        path_components.append("db")
        return os.path.sep.join(path_components)


    def db_exists(self, path: str, db_name: str) -> bool:
        db_file_path = os.path.join(path, db_name)
        return os.path.exists(db_file_path)


    def create_db(self, path: str, db_name: str):
        if not os.path.exists(path):
            os.mkdir(path)

        connection = sqlite3.connect(os.path.join(path, db_name))
        cursor = connection.cursor()
        create_db_sqls = [
            '''
                CREATE TABLE IF NOT EXISTS store (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL CHECK(length(name) <= 30),
        	        date_created DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS account (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL CHECK(length(name) <= 30),
                    store_id INTEGER,
        	        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (store_id) REFERENCES store(id),
                    UNIQUE(name, store_id)
                )
            ''',
            '''
                CREATE TABLE IF NOT EXISTS password (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER,
        	        password TEXT NOT NULL,
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        	        FOREIGN KEY (account_id) REFERENCES account(id)
                )
            '''
        ]

        for command in create_db_sqls:
            cursor.execute(command)

        connection.commit()
        connection.close()


def main():
    parser = argparse.ArgumentParser(
        prog="safe-pm setup", description="Create a new database for storing passwords")

    parser.add_argument(
        "-n", "--name", type=str, help="name of the database to create", required=True)

    args = parser.parse_args()
    name = args.name

    setup = Setup(name)
    return_value = setup.do_setup()

    sys.exit(return_value)


if __name__ == "__main__":
    main()
    sys.exit(0)
