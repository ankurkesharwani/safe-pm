import sqlite3
import os
import getpass


class SetupManager:


    def __init__(self, db_path: str, db_name: str):
        self.db_path = db_path
        self.db_name = db_name


    def do_setup(self):
        if self.db_exists(self.db_path, self.db_name):
            print("Database already exists")
            return 1

        self.create_db(self.db_path, self.db_name)

        if self.db_exists(self.db_path, self.db_name):
            print("Database created successfully")
            return 0

        else:
            print("Error: Failed to create database")
            return 2


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
            ''',
            '''
                CREATE TABLE IF NOT EXISTS meta (
        	        salt TEXT NOT NULL,
                    password TEXT NOT NULL
                    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        	        UNIQUE(salt, password)
                )
            '''
        ]

        for command in create_db_sqls:
            cursor.execute(command)

        connection.commit()
        connection.close()
