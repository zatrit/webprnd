from ecdsa import SigningKey, VerifyingKey
from hashlib import sha256
from cryptography.fernet import Fernet
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Callable

TIME_BYTES = 8
ENCODING = "utf8"
KeyProvider = Callable[[str], VerifyingKey | None]


def fernet_for(key: str) -> Fernet:
    _hash = sha256(key.encode(ENCODING)).digest()
    return Fernet(urlsafe_b64encode(_hash))


def token_for(login: str, sign_key: SigningKey, expires: int, role: str):
    expires_bytes = expires.to_bytes(TIME_BYTES, "big")
    parts = expires_bytes, role.encode(), login.encode(ENCODING)

    raw_token: str = ":".join(map(bytes.decode, map(urlsafe_b64encode, parts)))
    signature: bytes = sign_key.sign(raw_token.encode(ENCODING))

    return urlsafe_b64encode(signature).decode(ENCODING) + ":" + raw_token


def decode_token(token: str):
    sign, *parts = token.split(":")
    expires, *decodable = map(urlsafe_b64decode, parts)
    expires = int.from_bytes(expires, "big")
    role, login = map(bytes.decode, decodable)
    raw_token = ":".join(parts)

    return sign, raw_token, expires, role, login,


def verify_token(token: str, roles: list[str], current_time: int, key_provider: KeyProvider) -> bool:
    try:
        sign, raw_token, expires, role, login = decode_token(token)

        if (expires <= current_time and expires) or (role not in roles):
            return False

        key: VerifyingKey | None = key_provider(login)

        valid = key and key.verify(urlsafe_b64decode(
            sign), raw_token.encode(ENCODING))
        return bool(valid)
    except:
        return False
