import getpass
import os
import sqlite3
from typing import Any

from pm.setup import DatabaseException
from pm.util.console_util import display_table_in_less_with_ansi
from pm.util.crypto_util import verify_password, get_deterministic_hash, \
    derive_encryption_key, encrypt, decrypt
from pm.util.path_util import file_exists_in_path, get_db_path, get_db_file_name


class StoreException(Exception):
    """Exception raised for errors during the setup process."""
    pass


def create_store_password(args: Any):
    """
    Creates a new store entry in the database.

    Args:
        args (Any): Command-line arguments containing:
            - `args.db`: Name of the database.

    Raises:
        StoreException: If encountered errors, such as:
            - The entered password is incorrect.
            - The database does not exist.
            - There is an error while inserting data into the database.
    """
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        password = getpass.getpass("Enter password:")

        # Verify account credentials
        if not verify_password(password, db_name):
            raise StoreException("Error: [Store] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise StoreException(f"Error: [Store] - The requested db with name {db_name} does not exist")

        # Create store
        with sqlite3.connect(os.path.join(get_db_path(), db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Save store in db
                hid = get_deterministic_hash(store)
                encrypted_name = encrypt(store, derive_encryption_key(password))
                connection = sqlite3.connect(os.path.join(db_path, db_file_name))
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO store (hid, name) VALUES ('{hid}', '{encrypted_name}')")
                connection.commit()

                # Print message on standard output
                print("Store created successfully!")
            except Exception as e:
                raise DatabaseException(f"Error: [Store] - {str(e)}")
            finally:
                if cursor:
                    cursor.close()
    except StoreException as e:
        raise e
    except Exception as e:
        raise StoreException("Error: [Store] - Could not create store") from e


def rename_store(args: Any):
    """
    Renames an existing store in the database.

    Args:
        args (Any): Command-line arguments containing:
            - `args.db`: Name of the database.
            - `args.store`: Current name of the store.
            - `args.new_name`: New name for the store.

    Raises:
        StoreException: If encountered errors, such as:
            - The entered password is incorrect.
            - The database does not exist.
            - There is an issue updating the store name in the database.
    """
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        new_name = args.new_name
        password = getpass.getpass("Enter password:")

        # Verify account credentials
        if not verify_password(password, db_name):
            raise StoreException("Error: [Store] - Entered password is incorrect.")
        if not file_exists_in_path(db_path, db_file_name):
            raise StoreException(f"Error: [Store] - The requested db with name {db_name} does not exist.")

        # Rename store
        with sqlite3.connect(os.path.join(get_db_path(), db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Rename store in db
                hid = get_deterministic_hash(store)
                new_hid = get_deterministic_hash(new_name)
                encrypted_newname = encrypt(new_name, derive_encryption_key(password))
                connection = sqlite3.connect(os.path.join(db_path, db_file_name))
                cursor = connection.cursor()
                cursor.execute(f"UPDATE store SET hid='{new_hid}', name='{encrypted_newname}' WHERE hid='{hid}'")
                connection.commit()

                # Print message on standard output
                print("Store renamed successfully!")
            except Exception as e:
                raise DatabaseException(f"Error: [Store] - {str(e)}")
            finally:
                if cursor:
                    cursor.close()
    except StoreException as e:
        raise e
    except Exception as e:
        raise StoreException("Error: [Store] - Could not rename store.") from e


def delete_store(args: Any):
    """
    Deletes a store from the database.

    Args:
        args (Any): Command-line arguments containing:
            - `args.db`: Name of the database.
            - `args.store`: Name of the store to be deleted.

    Raises:
        StoreException: If encountered errors, such as:
            - The entered password is incorrect.
            - The database does not exist.
            - There is an issue deleting the store entry from the database.
    """
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        password = getpass.getpass("Enter password:")

        # Verify account credentials
        if not verify_password(password, db_name):
            raise StoreException("Error: [Store] - Entered password is incorrect.")
        if not file_exists_in_path(db_path, db_file_name):
            raise StoreException(f"Error: [Store] - The requested db with name {db_name} does not exist.")

        # Delete store
        with sqlite3.connect(os.path.join(get_db_path(), db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Delete store in db
                hid = get_deterministic_hash(store)
                connection = sqlite3.connect(os.path.join(db_path, db_file_name))
                cursor = connection.cursor()
                cursor.execute(f"DELETE from store where hid='{hid}'")
                connection.commit()

                # Print message on standard output
                print("Store deleted successfully!")
            except Exception as e:
                raise DatabaseException(f"Error: [Store] - {str(e)}")
            finally:
                if cursor:
                    cursor.close()
    except StoreException as e:
        raise e
    except Exception as e:
        raise StoreException("Error: [Store] - Could not delete store.") from e


def list_stores(args: Any):
    """
    Lists all stores in the specified database.

    Args:
        args (Any): Command-line arguments containing:
            - `args.db`: Name of the database.

    Raises:
        StoreException: If encountered errors, such as:
            - The entered password is incorrect.
            - The database does not exist.
            - There is an issue retrieving stores.
    """
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        password = getpass.getpass("Enter password:")

        # Verify account credentials
        if not verify_password(password, db_name):
            raise StoreException("Error: [Store] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise StoreException(f"Error: [Store] - The requested db with name {db_name} does not exist")

        # Listing stores
        with sqlite3.connect(os.path.join(get_db_path(), db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store info from db
                cursor.execute("SELECT name, date_created FROM store")
                records = cursor.fetchall()

                # Format and display store info
                output = []
                for r in records:
                    output.append((decrypt(r[0], derive_encryption_key(password)), r[1]))
                display_table_in_less_with_ansi(header=("Store", "Created At"), rows=output)
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                if cursor is not None:
                    cursor.close()
    except StoreException as e:
        raise e
    except Exception as e:
        raise StoreException("Error: [Store] - Could not list stores") from e
