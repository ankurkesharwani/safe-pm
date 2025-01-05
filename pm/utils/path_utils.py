import os
import sys


class PathException(Exception):
    """Custom exception for path-related errors."""
    pass


def get_db_path() -> str:
    """
    Constructs the absolute path to the 'db' directory by locating the 'bin' directory
    in the script's path and navigating one level above it.

    Returns:
        str: The absolute path to the 'db' directory.

    Raises:
        PathException: If the 'bin' directory is not found or any error occurs.
    """
    try:
        script_path = sys.argv[0]
        levels_up = _find_dir_in_path(script_path, "bin") + 1
        if levels_up < 0:
            raise FileNotFoundError("Error: [Path] - Directory 'bin' not found in the script path.")
        return _get_relative_path(script_path, levels_up, "db")
    except Exception as e:
        raise PathException("Error: [Path] - Could not get db path.") from e


def file_exists_in_path(path: str, file_name: str) -> bool:
    """
    Checks whether a specified file exists in the given directory.

    Args:
        path (str): The directory path.
        file_name (str): The file name to check.

    Returns:
        bool: True if the file exists, False otherwise.

    Raises:
        PathException: If an error occurs during file existence check.
    """
    try:
        return os.path.exists(os.path.join(path, file_name))
    except Exception as e:
        raise PathException("Error: [Path] - Could not complete the operation.") from e


def file_exists(file_path: str) -> bool:
    """
    Checks whether a file exists at the given file path.

    Args:
        file_path (str): The absolute file path.

    Returns:
        bool: True if the file exists, False otherwise.

    Raises:
        PathException: If an error occurs during the file existence check.
    """
    try:
        return os.path.exists(file_path)
    except Exception as e:
        raise PathException("Error: [Path] - Could not complete the operation.") from e


def create_file_in_path_if_not_exists(path: str, file_name: str) -> bool:
    """
    Creates a file in the specified directory if it does not already exist.

    Args:
        path (str): The directory where the file should be created.
        file_name (str): The name of the file to create.

    Returns:
        bool: True if the file was created, False if it already existed.

    Raises:
        PathException: If an error occurs while creating the file.
    """
    try:
        return create_file_if_not_exists(os.path.join(path, file_name))
    except Exception as e:
        raise PathException("Error: [Path] - Could not create specified file.") from e


def create_file_if_not_exists(file_path: str) -> bool:
    """
    Creates a file at the specified file path if it does not already exist.

    Args:
        file_path (str): The absolute file path.

    Returns:
        bool: True if the file was created, False if it already existed.

    Raises:
        PathException: If an error occurs while creating the file.
    """
    try:
        if not file_exists(file_path):
            open(file_path, "x").close()
            return True
        return False
    except Exception as e:
        raise PathException("Error: [Path] - Could not create specified file.") from e


def get_config_file_path() -> str:
    """
    Retrieves the absolute path to the configuration file located in the user's home directory.

    Returns:
        str: The absolute path to the configuration file.

    Raises:
        PathException: If an error occurs while constructing the config file path.
    """
    try:
        return os.path.join(get_user_home(), ".safe-pm.conf")
    except Exception as e:
        raise PathException("Error: [Path] - Could not get config file path.") from e


def get_user_home() -> str:
    """
    Retrieves the current user's home directory.

    Returns:
        str: The absolute path to the user's home directory.

    Raises:
        PathException: If an error occurs while retrieving the home directory.
    """
    try:
        return os.path.expanduser("~")
    except Exception as e:
        raise PathException("Error: [Path] - Could not complete the operation.") from e


def ensure_path(path: str):
    """
    Ensures that the specified directory exists. Creates the directory if it does not exist.

    Args:
        path (str): The directory path.

    Raises:
        PathException: If an error occurs while creating the directory.
    """
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except Exception as e:
        raise PathException("Error: [Path] - Could not complete the operation.") from e


def remove_file_in_path(path: str, file_name: str):
    """
    Removes a file from the specified directory.

    Args:
        path (str): The directory containing the file.
        file_name (str): The name of the file to remove.

    Raises:
        PathException: If an error occurs while removing the file.
    """
    try:
        os.remove(os.path.join(path, file_name))
    except Exception as e:
        raise PathException("Error: [Path] - Could not remove the specified file.") from e


def remove_file(file_path: str):
    """
    Removes a file at the specified file path.

    Args:
        file_path (str): The absolute path to the file.

    Raises:
        PathException: If an error occurs while removing the file.
    """
    try:
        os.remove(file_path)
    except Exception as e:
        raise PathException("Error: [Path] - Could not remove the specified file.") from e


def get_rainbow_path() -> str:
    """
    Constructs the absolute path to the 'rainbow' directory by locating the 'pm' directory
    in the script's path and navigating one level below it.

    Returns:
        str: The absolute path to the 'rainbow' directory.

    Raises:
        PathException: If the 'pm' directory is not found or any error occurs.
    """
    try:
        script_path = sys.argv[0]
        levels_up = _find_dir_in_path(script_path, "pm") - 1
        if levels_up < 0:
            raise FileNotFoundError("Error: [Path] - Directory 'pm' not found in the script path.")
        return _get_relative_path(script_path, levels_up, "rainbow")
    except Exception as e:
        raise PathException("Error: [Path] - Could not complete the operation.") from e


# Private methods


def _find_dir_in_path(script_path: str, target_dir: str) -> int:
    """
    Finds the target directory in the given path and returns how many levels up it is from the script location.

    Args:
        script_path (str): The full script path.
        target_dir (str): The directory to find.

    Returns:
        int: The number of levels up to reach the target directory.
             Returns -1 if the directory is not found.
    """
    path_components = script_path.split(os.path.sep)
    try:
        return len(path_components) - path_components.index(target_dir) - 1
    except ValueError:
        return -1


def _get_relative_path(base_path: str, levels_up: int, append_dir: str) -> str:
    """
    Constructs an absolute path by moving up a specified number of levels and appending a directory.

    Args:
        base_path (str): The base file path.
        levels_up (int): The number of levels to go up.
        append_dir (str): The directory to append.

    Returns:
        str: The constructed absolute path.

    Raises:
        PathException: If an error occurs while constructing the path.
    """
    try:
        path_components = base_path.split(os.path.sep)
        if levels_up > len(path_components):
            raise ValueError("Error: [Path] - Cannot traverse up more levels than the path depth.")
        return os.path.join(os.path.sep.join(path_components[:-levels_up]), append_dir)
    except Exception as e:
        raise PathException("Error: [Path] - Could not get relative path.") from e
