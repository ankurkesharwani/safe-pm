from typing import Tuple

import bcrypt
import base64
import binascii


def generate_password_hash(password: str) -> Tuple[str, str] :
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return binascii.hexlify(salt).decode("utf-8"), hashed_password.decode("utf-8")