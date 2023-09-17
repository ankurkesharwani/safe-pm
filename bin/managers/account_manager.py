import getpass
import math
import sqlite3
import os
import sys
import random
import string
import re
import traceback

from .utils.crypto_utils import verify_password, encrypt, derive_encryption_key, decrypt, get_deterministic_hash
from .utils.path_utils import get_rainbow_path, file_exists_in_path

import random
import string


def generate_random_password(min_length,
                             max_length,
                             pass_no_special=False,
                             pass_no_digits=False,
                             pass_exclude_chars=""):

    if min_length is None:
        min_length = 8

    if max_length is None:
        max_length = 16

    if pass_no_special is None:
        pass_no_special = False

    if pass_no_digits is None:
        pass_no_digits = False

    if pass_exclude_chars is None:
        pass_exclude_chars = ""

    # Define all chars to use to generate the password
    letters_pool = "".join([c for c in string.ascii_letters if c not in pass_exclude_chars])
    digits_pool = "".join([c for c in string.digits if c not in pass_exclude_chars])
    special_chars_pool = "".join([c for c in "!@#$%^&*([{}])_+=<>?" if c not in pass_exclude_chars])
    valid_chars_pool = (
            letters_pool
            + (digits_pool if not pass_no_digits else "")
            + (special_chars_pool if not pass_no_special else "")
    )

    # Create a buffer to create password
    password = ""
    check_min_length = 0

    # Ensure that min and max lengths are correct
    if not pass_no_special and not pass_no_digits:
        check_min_length = max(min_length, 3)
    elif not pass_no_special:
        check_min_length = max(min_length, 1)
    elif not pass_no_digits:
        check_min_length = max(min_length, 1)
    check_max_length = max(check_min_length, max_length)

    # Decide the password length
    password_length = random.randint(check_min_length, check_max_length)

    # Ensure that at least one special char is in the password
    if not pass_no_special:
        password += random.choice(special_chars_pool)

    # Ensure that at least one digit is in the password
    if not pass_no_digits:
        password += random.choice(digits_pool)

    remaining_length = password_length - len(password)

    if remaining_length > 0:
        password += "".join(random.choice(valid_chars_pool) for _ in range(remaining_length))

    password_list = list(password)
    random.shuffle(password_list)
    password = "".join(password_list)

    return password


def calculate_password_strength(password):
    if len(password) == 0:
        return 0.0

    # Define a set of common patterns to check for in weak passwords
    weak_patterns = [
        r'\d+',
        r'[a-z]+[A-Z]+'
        r'[A-Z]+[a-z]+'
        r'[a-zA-Z]+',
        r'[a-zA-Z]+[0-9]+',
        r'[0-9]+[a-zA-Z]+'
        r'[a-zA-Z]+[0-9]+[@#$%^&*()_+=<>?]+',
        r'[a-zA-Z]+[@#$%^&*()_+=<>?]+[0-9]+',
        r'[0-9]+[a-zA-Z]+[@#$%^&*()_+=<>?]+',
        r'[0-9]+[@#$%^&*()_+=<>?]+[a-zA-Z]+',
        r'[@#$%^&*()_+=<>?]+[a-zA-Z]+[0-9]+',
        r'[@#$%^&*()_+=<>?]+[0-9]+[a-zA-Z]+',
    ]

    # Define a set of criteria to check for strong passwords
    strong_criteria = {
        "Length": len(password) >= 12,  # Minimum length
        "Lower case chars": any(char.islower() for char in password),  # Contains lowercase letters
        "Upper case chars": any(char.isupper() for char in password),  # Contains uppercase letters
        "Digits": any(char.isdigit() for char in password),  # Contains digits
        "Special Chars": any(char in "!@#$%^&*()_+=<>?" for char in password),  # Contains special characters
    }

    # Initialize the strength score
    strength = 0
    pattern_miss_cost = 5
    criteria_miss_cost = 2

    # Check for weak patterns and deduct points accordingly
    for pattern in weak_patterns:
        if re.fullmatch(pattern, password):
            print(f"{password} matches weak pattern {pattern}")
            strength -= pattern_miss_cost

    for k in strong_criteria.keys():
        if strong_criteria[k] is False:
            print(f"{password} does not match strong criteria {k}")
            strength -= criteria_miss_cost

    max_possible_cost = pattern_miss_cost + (4 * criteria_miss_cost)
    final_strength = ((max_possible_cost + strength) / max_possible_cost)
    return math.ceil(final_strength * 100) / 100


def edit_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)

    # Create a 2D array to store edit distances
    dp = [[0 for _ in range(len_str2 + 1)] for _ in range(len_str1 + 1)]

    # Initialize the first row and column
    for i in range(len_str1 + 1):
        dp[i][0] = i
    for j in range(len_str2 + 1):
        dp[0][j] = j

    # Define character replacements (e.g., 'a' or 'A' can be replaced by '@', 'o' or 'O' can be replaced by '0')
    replacements = {
        'a': '@',
        'A': '@',
        'e': '3',
        'i': '1',
        'I': '1',
        'o': '0',
        'O': '0',
        'p': '9',
        'P': '9',
        's': '$',
        'S': '$',
        't': '7',
        'T': '7',
        'z': '2',
        'Z': '2'
    }

    # Calculate edit distances
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0

            # Check if characters are different
            if str1[i - 1] != str2[j - 1]:
                # Check if characters can be replaced by similar-looking special chars or numbers
                if str1[i - 1] in replacements and replacements[str1[i - 1]] == str2[j - 1]:
                    cost = 1
                if str1[i - 1].lower() == str2[j - 1].lower():
                    cost = 0
                else:
                    cost = 3  # Default cost for other edits

            dp[i][j] = min(
                dp[i - 1][j] + 8,  # Deletion
                dp[i][j - 1] + 4,  # Insertion
                dp[i - 1][j - 1] + cost,  # Substitution
            )

    return dp[len_str1][len_str2]


def find_most_similar_password(password, rainbow_table):
    min_distance = float('inf')
    most_similar_password = None

    for entry in rainbow_table:
        distance = edit_distance(password, entry)
        if distance < min_distance:
            min_distance = distance
            most_similar_password = entry

    return most_similar_password, min_distance


class AccountManager:

    def __init__(self, db_path: str, db_name: str):
        self.db_path = db_path
        self.db_name = db_name

    def list_accounts(self, db_name: str, store_name: str) -> None:
        pass

    def create_account(self,
                       store_name: str,
                       account_name: str,
                       username: str,
                       email: str,
                       use_password: bool = False,
                       auto_gen_password: bool = False,
                       pass_min_length: int = None,
                       pass_max_length: int = None,
                       pass_no_special: bool = False,
                       pass_no_digits: bool = False,
                       pass_exclude_chars: str = None) -> int:

        password_to_save = None
        if use_password:
            password_to_save = getpass.getpass("Enter password to save for this account:")

            # Generate a rainbow table
            rainbow_table = []
            with open(get_rainbow_path(), "r") as file:
                for line in file:
                    rainbow_table.append(line.strip())

            strength = calculate_password_strength(password_to_save)
            rainbow_match, distance = find_most_similar_password(password_to_save, rainbow_table)
            print(f"You have chosen a password with strength: {strength}")
            if rainbow_match is not None and distance < 5:
                print(f"Your chosen password is very similar to a dictionary password '{rainbow_match}'")

        elif auto_gen_password:
            password_to_save = generate_random_password(
                pass_min_length, pass_max_length, pass_no_special, pass_no_digits, pass_exclude_chars)

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
            store_hid = get_deterministic_hash(store_name)
            account_hid = get_deterministic_hash(account_name)
            encrypted_account_name = encrypt(account_name, derive_encryption_key(password))
            encrypted_password_to_save = encrypt(password_to_save, derive_encryption_key(password))

            encrypted_username = None
            if username is not None:
                encrypted_username = encrypt(username, derive_encryption_key(password))

            encrypted_email = None
            if email is not None:
                encrypted_email =  encrypt(email, derive_encryption_key(password))

            # Open db connection
            connection = sqlite3.connect(os.path.join(self.db_path, self.db_name))
            cursor = connection.cursor()

            # Get the store id
            db_result = cursor.execute(f"SELECT id FROM store WHERE hid='{store_hid}'")
            store_id_record = db_result.fetchone()
            if store_id_record is None:
                raise Exception("Store does not exists.")
            store_id = store_id_record[0]

            # Save account and password
            cursor.execute(f"INSERT INTO account (hid, name, username, email, store_id) "
                           f"VALUES ('{account_hid}', '{encrypted_account_name}', '{encrypted_username}', '{encrypted_email}', '{store_id}')")
            account_id = cursor.lastrowid
            cursor.execute(f"INSERT INTO password (account_id, password) VALUES ('{account_id}', '{encrypted_password_to_save}')")

            # Commit db
            connection.commit()
        except Exception as e:
            print("Error:", e)

            return 1
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()



    def view_account(self, db_name: str, store_name: str, account_name: str, view_type: str) -> None:
        pass

    def copy_account(self, db_name: str, store_name: str, account_name: str, copy_type: str) -> None:
        pass

    def update_account(self,
                       db_name: str,
                       store_name: str,
                       account_name: str,
                       password: str = None,
                       auto_gen_password: bool = False,
                       pass_min_length: int = None,
                       pass_max_length: int = None,
                       pass_no_special: bool = False,
                       pass_no_digits: bool = False,
                       pass_exclude_chars: str = None) -> None:
        pass

    def delete_account(self, db_name: str, store_name: str, account_name: str) -> None:
        pass

    def account_history(self, db_name: str, store_name: str, account_name: str) -> None:
        pass
