"""Функции для работы с токенами авторизации.
Логины, хэши паролей и т.д. должны передаваться как bytes"""
from cryptography.fernet import Fernet
import base64
from hashlib import sha256


def __concatenate(*hashes: bytes) -> int:
    to_mod, *to_sum = sorted(map(int.from_bytes, hashes))
    return sum(to_sum) % to_mod


def __fernet_for(login: bytes) -> Fernet:
    rev_login = bytes(reversed(login))
    rev_login_hash = sha256(rev_login).digest()
    b64_rev_login = base64.urlsafe_b64encode(rev_login_hash)

    return Fernet(b64_rev_login)


def __unencryped_token(login_hash: bytes, password_hash: bytes) -> bytes:
    return __concatenate(login_hash, password_hash).to_bytes(32, "big")


def token_for(login: bytes, password_hash: bytes) -> bytes:
    fernet = __fernet_for(login)

    login_hash = sha256(login).digest()
    summ = __unencryped_token(login_hash, password_hash)

    return fernet.encrypt(summ)


def validate(token: bytes, login: bytes, password_hash: bytes) -> bool:
    try:
        fernet = __fernet_for(login)

        decrypted_token = fernet.decrypt(token)

        login_hash = sha256(login).digest()
        summ = __concatenate(login_hash, password_hash).to_bytes(32, "big")

        return summ == decrypted_token
    except:
        return False
