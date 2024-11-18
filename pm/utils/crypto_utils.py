from typing import Tuple
import bcrypt
import base64
import binascii


def generate_password_hash(password: str) -> Tuple[str, str]:
    """
    Generates a hashed password and salt for the provided plaintext password.

    This function uses the bcrypt hashing algorithm to securely hash the password.
    The salt is generated using `bcrypt.gensalt()` and then combined with the password
    to produce a secure hash. The salt is returned in a hexadecimal string format.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        Tuple[str, str]: A tuple containing:
            - The hashed password (in bytes).
            - The salt used for hashing (hex-encoded string).

    Raises:
        ValueError: If the password is empty or invalid.
    """
    if not password:
        raise ValueError("Password cannot be empty.")

    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return the salt (hex-encoded) and the hashed password
    return hashed_password.decode("utf-8"), binascii.hexlify(salt).decode("utf-8")
