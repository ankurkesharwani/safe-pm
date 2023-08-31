import os
import sys


def get_db_path() -> str:
    script_path = sys.argv
    path_components = script_path[0].split(os.path.sep)[:-2]
    path_components.append("db")
    return os.path.sep.join(path_components)


def file_exists_in_path(dir_path: str, file_name: str) -> bool:
    file_path = os.path.join(dir_path, file_name)
    return os.path.exists(file_path)


def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def create_file_in_path_if_not_exists(dir_path: str, file_name: str) -> bool:
    full_path = os.path.join(dir_path, file_name)

    try:
        with open(full_path, "x"):
            return True
    except IOError:
        return False


def create_file_if_not_exists(file_path: str) -> bool:
    try:
        with open(file_path, "x"):
            return True
    except IOError:
        return False


def get_user_home() -> str:
    return os.path.expanduser("~")


def get_config_file_path() -> str:
    return os.path.join(get_user_home(), ".safe-pm.conf")


def ensure_path(dir_path: str):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def remove_file_in_path(dir_path: str, file_name: str):
    os.remove(os.path.join(dir_path, file_name))


def remove_file(file_name: str):
    os.remove(file_name)
