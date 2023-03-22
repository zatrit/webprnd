"""Функции для работы с токенами авторизации.
Логины, хэши паролей и т.д. должны передаваться как bytes"""
from cryptography.fernet import Fernet
import base64
from hashlib import sha256


def _concatenate(*hashes: bytes) -> int:
    return sum(map(lambda _hash: int.from_bytes(_hash, "big"), hashes))


def _fernet_for(login: bytes):
    rev_login = bytes(reversed(login))
    rev_login_hash = sha256(rev_login).digest()
    b64_rev_login = base64.urlsafe_b64encode(rev_login_hash)

    return Fernet(b64_rev_login)


def __unencryped_token(login_hash: bytes, password: bytes):
    return _concatenate(login_hash, password).to_bytes(33, "big")


def token_for(login: bytes, password: bytes):
    fernet = _fernet_for(login)

    login_hash = sha256(login).digest()
    summ = __unencryped_token(login_hash, password)

    return fernet.encrypt(summ)


def validate(token: bytes, login: bytes, password: bytes):
    try:
        fernet = _fernet_for(login)

        decrypted_token = fernet.decrypt(token)

        login_hash = sha256(login).digest()
        summ = _concatenate(login_hash, password).to_bytes(33, "big")

        return summ == decrypted_token
    except:
        return False
