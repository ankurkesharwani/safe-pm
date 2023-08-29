import os
import sys


def get_db_path() -> str:
    script_path = sys.argv
    path_components = script_path[0].split(os.path.sep)[:-2]
    path_components.append("db")
    return os.path.sep.join(path_components)
