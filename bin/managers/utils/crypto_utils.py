import base64
import binascii

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from .config_utils import get_password_hash_and_salt
from .path_utils import get_config_file_path


def generate_password_hash(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return binascii.hexlify(salt).decode("utf-8"), hashed_password.decode("utf-8")


def verify_password(password: str, db_name: str):
    password_hash, salt = get_password_hash_and_salt(get_config_file_path(), db_name)
    return verify_password_hash(password, password_hash, salt)


def verify_password_hash(entered_password: str, password_hash: str, salt: str) -> bool:
    hashed_password = bcrypt.hashpw(entered_password.encode('utf-8'), binascii.unhexlify(salt))
    return hashed_password.decode("utf-8") == password_hash


def derive_encryption_key(password: str):
    salt = hashes.Hash(hashes.SHA256(), backend=default_backend())
    salt.update(password.encode("utf-8"))
    derived_salt = salt.finalize()

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
    encoded_key = base64.urlsafe_b64encode(key)

    return encoded_key


def encrypt(data: str, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.encrypt(data.encode("utf-8")).decode("utf-8")


def decrypt(data: str, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(data.encode("utf-8")).decode("utf-8")
