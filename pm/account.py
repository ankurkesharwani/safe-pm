import getpass
import os
import sqlite3

from pm.setup import DatabaseException
from pm.util.crypto_util import verify_password, get_deterministic_hash, \
    encrypt, derive_encryption_key
from pm.util.password_util import generate_random_password
from pm.util.path_util import file_exists_in_path, get_db_path


class AccountException(Exception):
    pass


def list_accounts(args):
    pass


def create_account(args):
    try:
        db_path = get_db_path()
        db = args.db
        store = args.store
        account = args.account
        username = args.username
        email = args.email
        set_user_password = args.password
        set_auto_gen_password = args.auto_gen_password
        password_min_length = args.pass_min_length
        password_max_length = args.pass_max_length
        use_no_special_chars = args.pass_no_special
        use_no_digits = args.pass_no_digits
        exclude_chars = args.pass_exclude_chars

        # Get the password to save
        selected_password = None
        if set_user_password:
            selected_password = getpass.getpass("Enter password to save for this account:")
        elif set_auto_gen_password:
            selected_password = generate_random_password(password_min_length, password_max_length, use_no_special_chars, use_no_digits, exclude_chars)
        else:
            pass

        # Confirm store password
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db):
            raise AccountException("Error: [Account] - Entered password is incorrect")

        if not file_exists_in_path(db_path, db):
            raise AccountException(f"Error: [Account] - The requested db with name {db} does not exist")

        # Encrypt values to save
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        encrypted_account_name = encrypt(account, encryption_key)
        encrypted_password_to_save = encrypt(selected_password, encryption_key)
        encrypted_username = encrypt(username, encryption_key) if username is not None else None
        encrypted_email = encrypt(email, encryption_key) if email is not None else None

        # Same in db
        with sqlite3.connect(os.path.join(db_path, db)) as connection:
            cursor = connection.cursor()
            try:
                # Get the store id
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Save account and password
                cursor.execute(
                    f"INSERT INTO account (hid, name, username, email, store_id) "
                    f"VALUES ('{account_hid}', '{encrypted_account_name}', '{encrypted_username}', '{encrypted_email}', '{store_id}')")
                account_id = cursor.lastrowid
                cursor.execute(f"INSERT INTO password (account_id, password) VALUES ('{account_id}', '{encrypted_password_to_save}')")

                # Commit db
                connection.commit()
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                cursor is not None and cursor.close()
                connection is not None and connection.close()

    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Error: [Account] - Could not create new account in store.")


def view_account_credentials(args):
    pass


def copy_account_credentials(args):
    pass


def update_account(args):
    pass


def delete_account(args):
    pass


def view_account_history(args):
    pass