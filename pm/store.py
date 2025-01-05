import getpass
import os
import sqlite3
from typing import Any

from pm.setup import DatabaseException
from pm.utils.crypto_utils import verify_password, get_deterministic_hash, derive_encryption_key, encrypt
from pm.utils.path_utils import file_exists_in_path, get_db_path


class StoreException(Exception):
    """Exception raised for errors during the setup process."""
    pass


def create_store_password(args: Any):
    try:
        db_path = get_db_path()
        db = args.db
        store = args.db
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db):
            raise StoreException("Error: [Store] - Entered password is incorrect")

        if not file_exists_in_path(db_path, db):
            raise StoreException(f"Error: [Store] - The requested db with name {db} does not exist")

        connection = None
        cursor = None
        try:
            hid = get_deterministic_hash(store)
            encrypted_name = encrypt(store, derive_encryption_key(password))
            connection = sqlite3.connect(os.path.join(db_path, db))
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO store (hid, name) VALUES ('{hid}', '{encrypted_name}')")
            cursor.execute("INSERT INTO version DEFAULT VALUES")
            connection.commit()
        except Exception as e:
            raise DatabaseException(f"Error: [Store] - {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        print("Store created successfully!")
    except StoreException as e:
        raise e
    except Exception as e:
        raise StoreException("Error: [Store] - Could not create store") from e

def rename_store(args: Any):
    print(args)


def delete_store(args: Any):
    print(args)


def list_stores(args: Any):
    try:
        db_path = get_db_path()
        db = args.db
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db):
            raise StoreException("Error: [Store] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db):
            raise StoreException(f"Error: [Store] - The requested db with name {db} does not exist")
    except StoreException as e:
        raise e
    except Exception as e:
        raise StoreException("Error: [Store] - Could not list stores") from e
