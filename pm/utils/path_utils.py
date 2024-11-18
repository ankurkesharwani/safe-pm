import os
import sys


def get_db_path() -> str:
    """
    Constructs the file path to the database directory by finding the target directory in the script's path.

    Returns:
        str: The absolute path to the database directory.
    """
    script_path = sys.argv[0]
    levels_up = find_dir_in_path(script_path, "pm") - 1
    if levels_up < 0:
        raise FileNotFoundError(f"Directory pm not found in the script path.")
    return get_relative_path(script_path, levels_up, "db")


def file_exists_in_path(path: str, file_name: str) -> bool:
    """
    Checks if a specified file exists within a given directory.

    Args:
        path (str): The directory path.
        file_name (str): The name of the file to check for.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    file_path = os.path.join(path, file_name)
    return os.path.exists(file_path)


def file_exists(file_path: str) -> bool:
    """
    Checks if a file exists at a specified file path.

    Args:
        file_path (str): The absolute file path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


def create_file_in_path_if_not_exists(path: str, file_name: str) -> bool:
    """
    Creates a file in the specified directory if it does not already exist.

    Args:
        path (str): The directory where the file should be created.
        file_name (str): The name of the file to create.

    Returns:
        bool: True if the file was created, False if it already existed.
    """
    file_path = os.path.join(path, file_name)
    return create_file_if_not_exists(file_path)


def create_file_if_not_exists(file_path: str) -> bool:
    """
    Creates a file at the specified file path if it does not already exist.

    Args:
        file_path (str): The absolute path to the file to create.

    Returns:
        bool: True if the file was created, False if it already existed.
    """
    if not file_exists(file_path):
        open(file_path, "x").close()
        return True
    return False


def get_config_file_path() -> str:
    """
    Retrieves the file path to the configuration file located in the user's home directory.

    Returns:
        str: The absolute path to the configuration file.
    """
    return os.path.join(get_user_home(), ".safe-pm.conf")


def get_user_home() -> str:
    """
    Gets the current user's home directory.

    Returns:
        str: The absolute path to the user's home directory.
    """
    return os.path.expanduser("~")


def ensure_path(path: str):
    """
    Ensures that a directory exists. Creates the directory if it does not exist.

    Args:
        path (str): The path of the directory to ensure exists.
    """
    if not os.path.exists(path):
        os.mkdir(path)


def remove_file_in_path(path: str, file_name: str):
    """
    Removes a file from the specified directory.

    Args:
        path (str): The directory containing the file.
        file_name (str): The name of the file to remove.
    """
    os.remove(os.path.join(path, file_name))


def remove_file(file_path: str):
    """
    Removes a file at the specified file path.

    Args:
        file_path (str): The absolute path to the file to remove.
    """
    os.remove(file_path)


def get_rainbow_path() -> str:
    """
    Constructs the file path to the 'rainbow' directory by navigating two levels up
    from the script's directory and appending 'rainbow' to the path.

    Returns:
        str: The absolute path to the 'rainbow' directory.
    """
    script_path = sys.argv[0]
    levels_up = find_dir_in_path(script_path, "pm") - 1
    if levels_up < 0:
        raise FileNotFoundError(f"Directory pm not found in the script path.")
    return get_relative_path(script_path, levels_up, "rainbow")


def find_dir_in_path(script_path: str, target_dir: str) -> int:
    """
    Finds the target directory in the given path and returns how many levels up it is from the current directory.

    Args:
        script_path (str): The full script path to search within.
        target_dir (str): The directory to find in the path.

    Returns:
        int: The number of levels up to reach the target directory.
             Returns -1 if the directory is not found.
    """
    path_components = script_path.split(os.path.sep)
    try:
        target_index = path_components.index(target_dir)
        return len(path_components) - target_index - 1
    except ValueError:
        return -1


def get_relative_path(base_path: str, levels_up: int, append_dir: str) -> str:
    """
    Constructs a relative path by traversing up a specified number of levels and appending a directory.

    Args:
        base_path (str): The starting path to traverse from.
        levels_up (int): The number of levels to traverse up.
        append_dir (str): The directory to append after traversing up.

    Returns:
        str: The constructed relative path.
    """
    path_components = base_path.split(os.path.sep)
    if levels_up > len(path_components):
        raise ValueError("Cannot traverse up more levels than the path depth.")
    target_path = os.path.sep.join(path_components[:-levels_up])
    return os.path.join(target_path, append_dir)


