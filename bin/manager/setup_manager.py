import sqlite3
import os


class SetupManager:


    def do_setup(self, db_path: str, name: str):
        if self.db_exists(db_path, name):
            print("Database already exists")
            return 1

        self.create_db(db_path, name)

        if self.db_exists(db_path, name):
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
            '''
        ]

        for command in create_db_sqls:
            cursor.execute(command)

        connection.commit()
        connection.close()
