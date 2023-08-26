import sqlite3
import os
import sys


class StoreManager:


    def create_store(self, name: str):
        print(f"Create store {name}")


    def rename_store(self, old_name: str, new_name: str):
        print(f"Rename store {old_name} to {new_name}")


    def delete_store(self, name: str):
        print(f"Deleting store with name: {name}")


    def list_stores(self):
        print("Listing all stores")
