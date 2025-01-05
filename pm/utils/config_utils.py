from typing import Tuple


class ConfigException(Exception):
    pass


def update_config(file_path: str, db: str, password_hash: str, salt: str) -> None:
    """
    Updates the configuration file with a new database entry or updates an existing one.

    This function ensures that each database entry in the configuration file is unique.
    It rewrites the file to exclude any existing entry for the specified database and
    appends the new or updated entry at the end.

    Args:
        file_path (str): The path to the configuration file.
        db (str): The database name to be added or updated.
        password_hash (str): The password hash associated with the database.
        salt (str): The salt used to hash the password.

    Raises:
        ConfigException: If there are issues reading or writing to the configuration file.
    """
    if not file_path or not db or not password_hash or not salt:
        raise ConfigException("Error: [Config] - File path, database name, password hash, and salt cannot be empty.")

    try:
        # Read existing config
        updated_lines = []
        with open(file_path, 'r') as file:
            # Read all lines and filter out the current database entry
            lines = file.readlines()
            for line in lines:
                if not line.startswith(db):
                    updated_lines.append(line.strip())
            file.close()

        # Append the new entry
        updated_lines.append(f"{db}:{password_hash},{salt}")
        with open(file_path, 'w') as file:
            for line in updated_lines:
                file.write(line + "\n")
            file.close()
    except Exception as e:
        raise ConfigException("Error: [Config] - Could not complete the operation.") from e


def get_password_hash_and_salt(file_path: str, db: str) -> Tuple[str, str]:
    """
    Retrieves the password hash and salt for a given database from the configuration file.

    This function searches the configuration file for an entry matching the database name
    and extracts the associated password hash and salt values.

    Args:
        file_path (str): The path to the configuration file.
        db (str): The database name for which the password hash and salt are to be retrieved.

    Returns:
        Tuple[str, str]: A tuple containing the password hash and salt.

    Raises:
        ConfigException: If there are issues reading the configuration file.
    """
    if not file_path or not db:
        raise ConfigException("Error: [Config] - File path and database name cannot be empty.")

    try:
        selected_line = None
        with open(file_path, 'r') as file:
            # Search for the line corresponding to the database
            lines = file.readlines()
            for line in lines:
                if line.startswith(db):
                    selected_line = line
                    break
            file.close()

        if not selected_line:
            raise ValueError(f"Error: [Config] - Database entry for '{db}' not found in the configuration file.")

        components = selected_line.strip().split(":")[1].split(",")
        return components[0], components[1]
    except Exception as e:
        raise ConfigException("Error: [Config] - Could not complete the operation.") from e