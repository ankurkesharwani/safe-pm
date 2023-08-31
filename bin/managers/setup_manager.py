import getpass
import sqlite3
import os

from .utils.path_utils import *
from .utils.crypto_utils import *
from .utils.config_utils import *


def create_db(path: str, db_name: str):
    ensure_path(path)

    connection = sqlite3.connect(os.path.join(path, db_name))
    cursor = connection.cursor()
    create_db_sqls = [
        '''
            CREATE TABLE IF NOT EXISTS store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(length(name) <= 30),
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name)
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
        ''',
        '''
            CREATE TABLE IF NOT EXISTS version (
                version INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''',
        '''
            INSERT INTO version DEFAULT VALUES
        '''
    ]

    for command in create_db_sqls:
        cursor.execute(command)

    connection.commit()
    connection.close()


class SetupManager:

    def __init__(self, db_path: str, db_name: str):
        self.db_path = db_path
        self.db_name = db_name

    def do_setup(self):
        password = getpass.getpass("Enter master password for this db:")
        salt, password_hash = generate_password_hash(password)

        if salt is None or password_hash is None:
            print("Error: Cannot create db")
            return 4

        if file_exists_in_path(self.db_path, self.db_name):
            print("Error: Database already exists")
            return 1

        create_db(self.db_path, self.db_name)

        if not file_exists_in_path(self.db_path, self.db_name):
            print("Error: Failed to create database")
            return 2

        try:
            create_file_if_not_exists(get_config_file_path())
            update_config(get_config_file_path(), self.db_name, password_hash, salt)
        except IOError:
            remove_file_in_path(self.db_path, self.db_name)
            print("Error: Failed to create database")
            return 3

        print("Database created successfully!")
        return 0
