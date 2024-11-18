import getpass
import sqlite3
import os
from typing import Any

from pm.utils.config_utils import update_config
from pm.utils.path_utils import (
    ensure_path,
    file_exists_in_path,
    get_db_path,
    create_file_if_not_exists,
    get_config_file_path,
    remove_file_in_path
)
from pm.utils.crypto_utils import generate_password_hash


class SetupException(Exception):
    """Exception raised for errors during the setup process."""
    pass


class DatabaseException(Exception):
    """Exception raised for database-related errors."""
    pass


def setup_safe(args: Any) -> None:
    """
    Sets up the secure database by validating inputs, creating a new database,
    and storing the necessary configuration.

    Args:
        args (Any): Command-line arguments containing database information.

    Raises:
        SetupException: If any step in the setup process fails.
    """
    password = getpass.getpass("Enter master password for this db:")
    password_hash, salt  = generate_password_hash(password)

    if not salt or not password_hash:
        raise SetupException("Cannot create database. Could not securely create password hash or salt.")

    db_path = get_db_path()
    if file_exists_in_path(db_path, args.db):
        raise SetupException(f"Cannot create database. A database with the name '{args.db}' already exists.")

    create_db(db_path, args.db)

    if not file_exists_in_path(db_path, args.db):
        raise SetupException("Failed to create database.")

    try:
        config_file = get_config_file_path()
        create_file_if_not_exists(config_file)
        update_config(config_file, args.db, password_hash, salt)
    except IOError as e:
        remove_file_in_path(db_path, args.db)
        raise SetupException(f"Failed to create database. Error creating config: {e}")

    print("Database created successfully!")


def create_db(path: str, db_name: str) -> None:
    """
    Creates a SQLite database with predefined tables and inserts initial data.

    Args:
        path (str): The directory where the database should be created.
        db_name (str): The name of the database file.

    Raises:
        DatabaseException: If the database creation or initialization fails.
    """
    ensure_path(path)

    db_file_path = os.path.join(path, db_name)
    create_db_sqls = [
        '''
            CREATE TABLE IF NOT EXISTS store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hid TEXT NOT NULL,
                name TEXT NOT NULL,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(hid)
            )
        ''',
        '''
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY,
                hid TEXT NOT NULL,
                name TEXT NOT NULL,
                username TEXT DEFAULT NULL,
                email TEXT DEFAULT NULL,
                store_id INTEGER,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (store_id) REFERENCES store(id),
                UNIQUE(name, store_id),
                UNIQUE(hid)
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

    try:
        with sqlite3.connect(db_file_path) as connection:
            cursor = connection.cursor()
            for sql in create_db_sqls:
                cursor.execute(sql)
            connection.commit()
    except sqlite3.Error as e:
        raise DatabaseException(f"Could not create the database: {e}")
