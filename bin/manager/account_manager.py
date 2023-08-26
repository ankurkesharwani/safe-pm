import sqlite3
import os
import sys


class AccountManager:


    def __init__(self):
        pass


    def list_accounts(self, db_name: str, store_name: str) -> None:
        pass


    def create_account(self, db_name: str,
                       store_name: str,
                       account_name: str,
                       username: str,
                       email: str,
                       password: str = None,
                       auto_gen_password: bool = False,
                       pass_min_length: int = None,
                       pass_max_length: int = None,
                       pass_no_special: bool = False,
                       pass_no_digits: bool = False,
                       pass_exclude_chars: str = None) -> None:
        pass


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
