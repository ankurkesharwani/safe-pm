import getpass
import sqlite3

from .utils.console_utils import *
from .utils.crypto_utils import *
from .utils.path_utils import *


class StoreManager:

    def __init__(self, db_path: str, db_name: str):
        self.db_path = db_path
        self.db_name = db_name

    def create_store(self, name: str):
        password = getpass.getpass("Enter password:")
        if not verify_password(password, self.db_name):
            print("Error: Entered password is incorrect")
            return 1

        if not file_exists_in_path(self.db_path, self.db_name):
            print(f"Error: The requested db with name {self.db_name} does not exist")
            return 1

        connection = None
        cursor = None
        try:
            encrypted_name = encrypt(name, derive_encryption_key(password))
            connection = sqlite3.connect(os.path.join(self.db_path, self.db_name))
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO store (name) VALUES ('{encrypted_name}')")
            cursor.execute("INSERT INTO version DEFAULT VALUES")
            connection.commit()
        except Exception as e:
            print("Error:", e)

            return 1
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        print("Store created successfully!")
        return 0

    def rename_store(self, old_name: str, new_name: str):
        password = getpass.getpass("Enter password:")
        if not verify_password(password, self.db_name):
            print("Error: Entered password is incorrect")
            return 1

        if not file_exists_in_path(self.db_path, self.db_name):
            print(f"Error: The requested db with name {self.db_name} does not exist")
            return 1

        connection = None
        cursor = None
        try:
            encrypted_newname = encrypt(new_name, derive_encryption_key(password))
            encrypted_oldname = encrypt(old_name, derive_encryption_key(password))
            connection = sqlite3.connect(os.path.join(self.db_path, self.db_name))
            cursor = connection.cursor()
            cursor.execute(f"UPDATE store SET name='{encrypted_newname}' WHERE name='{encrypted_oldname}'")
            cursor.execute("INSERT INTO version DEFAULT VALUES")
            connection.commit()
        except Exception as e:
            print("Error:", e)

            return 1
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return 0

    def delete_store(self, name: str):
        password = getpass.getpass("Enter password:")
        if not verify_password(password, self.db_name):
            print("Error: Entered password is incorrect")
            return 1

        if not verify_password(getpass.getpass("Enter password:"), self.db_name):
            print("Error: Entered password is incorrect")
            return 1

        if not file_exists_in_path(self.db_path, self.db_name):
            print(f"Error: The requested db with name {self.db_name} does not exist")
            return 1

        connection = None
        cursor = None
        try:
            encrypted_name = encrypt(name, derive_encryption_key(password))
            connection = sqlite3.connect(os.path.join(self.db_path, self.db_name))
            cursor = connection.cursor()
            cursor.execute(f"DELETE from store where name='{encrypted_name}'")
            connection.commit()
        except Exception as e:
            print("Error:", e)
            return 1
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        print("Store deleted successfully!")
        return 0

    def list_stores(self):
        password = getpass.getpass("Enter password:")
        if not verify_password(password, self.db_name):
            print("Error: Entered password is incorrect")
            return 1

        if not file_exists_in_path(self.db_path, self.db_name):
            print(f"Error: The requested db with name {self.db_name} does not exist")
            return 1

        connection = None
        cursor = None
        try:
            connection = sqlite3.connect(os.path.join(self.db_path, self.db_name))
            cursor = connection.cursor()
            cursor.execute("SELECT name, date_created FROM store")
            records = cursor.fetchall()

            output = [("Store", "Created At")]
            for r in records:
                output.append((decrypt(r[0], derive_encryption_key(password)), r[1]))
            print_table(output)
        except Exception as e:
            print("Error:", e)
            return 1
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return 0
