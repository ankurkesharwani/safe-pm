from typing import Tuple
import bcrypt
import base64
import binascii

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pm.utils.config_utils import get_password_hash_and_salt
from pm.utils.path_utils import get_config_file_path


class CryptoException(Exception):
    """Custom exception class for cryptographic operations."""
    pass


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
        CryptoException: If hashing fails due to any error.
    """
    try:
        if not password:
            raise ValueError("Password cannot be empty.")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode("utf-8"), binascii.hexlify(salt).decode("utf-8")
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not generate password") from e


def verify_password(password: str, db_name: str) -> bool:
    """
    Verifies if the entered password matches the stored password hash.

    This function retrieves the stored password hash and salt from the configuration
    file and checks if the entered password, when hashed with the stored salt,
    matches the stored hash.

    Args:
        password (str): The plaintext password entered by the user.
        db_name (str): The database name associated with the stored password.

    Returns:
        bool: True if the password matches, False otherwise.

    Raises:
        CryptoException: If verification fails due to configuration errors.
    """
    try:
        password_hash, salt = get_password_hash_and_salt(get_config_file_path(), db_name)
        return verify_password_hash(password, password_hash, salt)
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not verify password") from e


def verify_password_hash(entered_password: str, password_hash: str, salt: str) -> bool:
    """
    Verifies if the entered password matches the given hash using the provided salt.

    Args:
        entered_password (str): The plaintext password entered by the user.
        password_hash (str): The stored password hash.
        salt (str): The salt used for hashing, stored in hex format.

    Returns:
        bool: True if the password matches, False otherwise.

    Raises:
        CryptoException: If verification fails due to invalid salt format or other errors.
    """
    try:
        hashed_password = bcrypt.hashpw(entered_password.encode('utf-8'), binascii.unhexlify(salt))
        return hashed_password.decode("utf-8") == password_hash
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not verify password hash") from e


def get_deterministic_hash(text: str) -> str:
    """
    Generates a deterministic SHA-256 hash of the given text and encodes it in base64.

    Args:
        text (str): The input text to be hashed.

    Returns:
        str: The base64-encoded SHA-256 hash of the input text.

    Raises:
        CryptoException: If hashing fails.
    """
    try:
        hash_function = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_function.update(text.encode("utf-8"))
        return base64.urlsafe_b64encode(hash_function.finalize()).decode("utf-8")
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not generate deterministic hash") from e


def derive_encryption_key(password: str) -> bytes:
    """
    Derives a 256-bit encryption key from the given password using the Scrypt key derivation function.

    Args:
        password (str): The password from which to derive the encryption key.

    Returns:
        bytes: The derived encryption key encoded in base64.

    Raises:
        CryptoException: If key derivation fails.
    """
    try:
        hash_function = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_function.update(password.encode("utf-8"))
        derived_salt = hash_function.finalize()

        n = 2 ** 16  # 65,536 iterations
        r = 8
        p = 1
        key_length = 32  # 256 bits for AES256

        kdf = Scrypt(
            salt=derived_salt,
            length=key_length,
            n=n,
            r=r,
            p=p,
            backend=default_backend()
        )

        key = kdf.derive(password.encode("utf-8"))
        return base64.urlsafe_b64encode(key)
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not derive encryption key") from e


def encrypt(data: str, key: bytes) -> str:
    """
    Encrypts the given data using AES encryption with the provided key.

    Args:
        data (str): The plaintext data to be encrypted.
        key (bytes): The encryption key.

    Returns:
        str: The encrypted data encoded in base64.

    Raises:
        CryptoException: If encryption fails.
    """
    try:
        fernet = Fernet(key)
        return fernet.encrypt(data.encode("utf-8")).decode("utf-8")
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not encrypt data") from e


def decrypt(data: str, key: bytes) -> str:
    """
    Decrypts the given encrypted data using AES decryption with the provided key.

    Args:
        data (str): The base64-encoded encrypted data to be decrypted.
        key (bytes): The encryption key used for decryption.

    Returns:
        str: The decrypted plaintext data.

    Raises:
        CryptoException: If decryption fails.
    """
    try:
        fernet = Fernet(key)
        return fernet.decrypt(data.encode("utf-8")).decode("utf-8")
    except Exception as e:
        raise CryptoException("Error: [Crypto] - Could not decrypt data") from e
