import getpass
import os
import sqlite3
import pyperclip

from pm.setup import DatabaseException
from pm.util.console_util import display_table_in_less_with_ansi
from pm.util.crypto_util import verify_password, get_deterministic_hash, encrypt, derive_encryption_key, decrypt
from pm.util.password_util import generate_random_password, calculate_password_strength, find_most_similar_password
from pm.util.path_util import file_exists_in_path, get_db_path, get_db_file_name, get_rainbow_table_path


class AccountException(Exception):
    pass


def list_accounts(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # Listing accounts
        store_hid = get_deterministic_hash(store)
        encryption_key = derive_encryption_key(password)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Fetch account records from db
                account_db_result = cursor.execute(f"SELECT * FROM account WHERE store_id='{store_id}'")
                account_records = account_db_result.fetchall()
                output = []
                for r in account_records:
                    output.append(
                        (
                            decrypt(r[2], encryption_key), decrypt(r[3], encryption_key), decrypt(r[4], encryption_key),
                            r[6]
                        )
                    )

                # Display in Less
                display_table_in_less_with_ansi(header=("Name", "Username", "Email", "Created At"), rows=output)
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                if cursor is not None:
                    cursor.close()
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Error: [Account] - Could not list accounts.") from e


def create_account(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
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

        # Configure password to save
        if set_user_password:
            # Get password from user
            selected_password = getpass.getpass("Enter password to save for this account:")

            # Generate a rainbow table
            rainbow_table = []
            with open(get_rainbow_table_path(), "r") as file:
                for line in file:
                    rainbow_table.append(line.strip())

            # Compute password strength
            strength = calculate_password_strength(selected_password)
            rainbow_match, distance = find_most_similar_password(selected_password, rainbow_table)
            print(f"You have chosen a password with strength: {strength}")
            if rainbow_match is not None and distance < 5:
                print(f"Your chosen password is very similar to a dictionary password '{rainbow_match}'")
        elif set_auto_gen_password:
            # Auto generate password
            selected_password = generate_random_password(
                password_min_length, password_max_length, use_no_special_chars, use_no_digits, exclude_chars
            )
        else:
            raise AccountException("Error: [Account] - Password to set cannot be empty.")

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # Create account
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        encrypted_account_name = encrypt(account, encryption_key)
        encrypted_password_to_save = encrypt(selected_password, encryption_key)
        encrypted_username = encrypt(username, encryption_key) if username is not None else encrypt("", encryption_key)
        encrypted_email = encrypt(email, encryption_key) if email is not None else encrypt("", encryption_key)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Save account and password
                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(
                    f"INSERT INTO account (hid, name, username, email, store_id) "
                    f"VALUES ("
                    f"  '{account_hid}', '{encrypted_account_name}', '{encrypted_username}', '{encrypted_email}', "
                    f"  '{store_id}'"
                    f")"
                )
                account_id = cursor.lastrowid
                cursor.execute(
                    f"INSERT INTO password (account_id, password) VALUES ("
                    f"  '{account_id}', '{encrypted_password_to_save}'"
                    f")"
                )
                connection.commit()

                # Print message on standard output
                print("Account created successfully!")
            except sqlite3.IntegrityError as e:
                raise AccountException(
                    "Error: [Account] - Could not create new account in store. "
                    "Please ensure that the account name is not previously set."
                )
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                if cursor is not None:
                    cursor.close()
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Error: [Account] - Could not create new account in store.")


def view_account_credentials(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        account = args.account

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # View account credentials
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Get account credentials from db
                account_db_result = cursor.execute(
                    f"SELECT * FROM account "
                    f"  JOIN password ON account.id=password.account_id "
                    f"WHERE account.store_id='{store_id}' "
                    f"  AND account.hid='{account_hid}' "
                    f"ORDER BY password.id DESC LIMIT 1"
                )
                account_records = account_db_result.fetchall()
                output = []
                for r in account_records:
                    output.append(
                        (
                            decrypt(r[2], encryption_key), decrypt(r[3], encryption_key), decrypt(r[4], encryption_key),
                            decrypt(r[9], encryption_key), r[10]
                        )
                    )

                # Display in Less
                display_table_in_less_with_ansi(
                    header=("Name", "Username", "Email", "Password", "Created At"), rows=output
                )
            except Exception as e:
                raise DatabaseException("Error: [Database] - Could not get account in the store.")
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Error: [Account] - Could not get account in the store.")


def copy_account_credentials(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        account = args.account
        field = args.field

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # View account credentials
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Get account credentials from db
                account_db_result = cursor.execute(
                    f"SELECT {field} FROM account "
                    f"  LEFT JOIN password ON account.id=password.id "
                    f"WHERE account.id='{store_id}' "
                    f"  AND account.hid='{account_hid}'"
                )
                account_records = account_db_result.fetchone()
                value = account_records[0]

                # Copy to clipboard
                pyperclip.copy(decrypt(value, encryption_key))

                # Print message on standard output
                print("Value copied to the clipboard.")
            except Exception as e:
                raise DatabaseException("Error: [Database] - Could not get account in the store.")
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Erorr: [Account] - Could not get account in the store.")


def update_account(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        account = args.account
        set_user_password = args.password
        set_auto_gen_password = args.auto_gen_password
        password_min_length = args.pass_min_length
        password_max_length = args.pass_max_length
        use_no_special_chars = args.pass_no_special
        use_no_digits = args.pass_no_digits
        exclude_chars = args.pass_exclude_chars

        # Configure password to save
        if set_user_password:
            # Get password from user
            selected_password = getpass.getpass("Enter password to save for this account:")

            # Generate a rainbow table
            rainbow_table = []
            with open(get_rainbow_table_path(), "r") as file:
                for line in file:
                    rainbow_table.append(line.strip())

            # Compute password strength
            strength = calculate_password_strength(selected_password)
            rainbow_match, distance = find_most_similar_password(selected_password, rainbow_table)
            print(f"You have chosen a password with strength: {strength}")
            if rainbow_match is not None and distance < 5:
                print(f"Your chosen password is very similar to a dictionary password '{rainbow_match}'")
        elif set_auto_gen_password:
            # Auto generate password
            selected_password = generate_random_password(
                password_min_length, password_max_length, use_no_special_chars, use_no_digits, exclude_chars
            )
        else:
            raise AccountException("Error: [Account] - Password to set cannot be empty.")

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # Create account
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        encrypted_password_to_save = encrypt(selected_password, encryption_key)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Get account id from db
                account_db_result = cursor.execute(
                    f"SELECT id FROM account WHERE hid='{account_hid}' AND store_id='{store_id}'"
                )
                account_id_record = account_db_result.fetchone()
                if account_id_record is None:
                    raise DatabaseException("Erorr: [Database] - Account does not exist in the store.")
                account_id = account_id_record[0]

                # Save new password
                cursor.execute(
                    f"INSERT INTO password (account_id, password) VALUES ("
                    f"  '{account_id}', '{encrypted_password_to_save}'"
                    f")"
                )
                connection.commit()

                # Print message on standard output
                print("Account updated successfully!")
            except sqlite3.IntegrityError as e:
                raise AccountException(
                    "Error: [Account] - Could not update account in store. "
                    "Please ensure that the account exists."
                )
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                if cursor is not None:
                    cursor.close()
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Error: [Account] - Could not update account in store.")


def delete_account(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        account = args.account

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # Delete account
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Get account id from db
                account_db_result = cursor.execute(f"SELECT * FROM account WHERE store_id='{store_id}' AND hid='{account_hid}'")
                account_record = account_db_result.fetchone()
                account_id = account_record[0]

                # Delete passwords and account from db
                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(f"DELETE FROM password WHERE account_id='{account_id}'")
                cursor.execute(f"DELETE FROM account WHERE store_id='{store_id}' AND hid='{account_hid}'")
                connection.commit()

                # Print message on standard output
                print("Account deleted successfully!")
            except sqlite3.IntegrityError as e:
                raise AccountException(
                    "Error: [Account] - Could not update account in store. "
                    "Please ensure that the account exists."
                )
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                if cursor is not None:
                    cursor.close()
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Error: [Account] - Could not delete the account from store.")


def view_account_history(args):
    try:
        # Read input params
        db_path = get_db_path()
        db_name = args.db
        db_file_name = get_db_file_name(db_name)
        store = args.store
        account = args.account

        # Verify account credentials
        password = getpass.getpass("Enter password:")
        if not verify_password(password, db_name):
            raise AccountException("Error: [Account] - Entered password is incorrect")
        if not file_exists_in_path(db_path, db_file_name):
            raise AccountException(f"Error: [Account] - The requested db with name {db_name} does not exist")

        # Delete account
        encryption_key = derive_encryption_key(password)
        store_hid = get_deterministic_hash(store)
        account_hid = get_deterministic_hash(account)
        with sqlite3.connect(os.path.join(db_path, db_file_name)) as connection:
            cursor = connection.cursor()
            try:
                # Get store id from db
                db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
                store_id_record = db_result.fetchone()
                if store_id_record is None:
                    raise DatabaseException("Error: [Database] - Store does not exists.")
                store_id = store_id_record[0]

                # Get account id from db
                account_db_result = cursor.execute(f"SELECT * FROM account WHERE store_id='{store_id}' AND hid='{account_hid}'")
                account_record = account_db_result.fetchone()
                account_id = account_record[0]

                # Get passwords from db
                password_db_result = cursor.execute(f"SELECT * from password WHERE account_id='{account_id}' ORDER BY id DESC")
                password_records = password_db_result.fetchall()
                output = []
                for r in password_records:
                    output.append(
                        (decrypt(r[2], encryption_key), r[3])
                    )
                
                # Display in less
                display_table_in_less_with_ansi(
                    header=("Password", "Created At"), rows=output
                )
            except sqlite3.IntegrityError as e:
                raise AccountException(
                    "Error: [Account] - Could not get account in store. "
                    "Please ensure that the account exists."
                )
            except Exception as e:
                raise DatabaseException(f"Error: [Database] - {str(e)}")
            finally:
                if cursor is not None:
                    cursor.close()
    except AccountException as e:
        raise e
    except Exception as e:
        raise AccountException("Erorr: [Account] - Could not get account in the store.")
