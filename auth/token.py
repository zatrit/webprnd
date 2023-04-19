from auth.crypto import token_for, verify_token
from ecdsa import VerifyingKey, SigningKey
from data.users import User
from time import time


def validate_token(token: str | None, roles: list[str]) -> bool:
    if not token:
        return False

    from data.db_session import create_session

    def key_provider(login: str):
        with create_session() as db_sess:
            user = db_sess.query(User).where(User.login == login).first()
            if user:
                return VerifyingKey.from_string(
                    user.verify_key)  # type: ignore

    return verify_token(token, roles, int(time()), key_provider)


def generate_token(user: User | None, password: str, lifetime: int = 0, role: str = "api") -> str | None:
    if not user:
        return None
    expires = 0 if not lifetime else (int(time()) + lifetime)

    try:
        sign_key = SigningKey.from_string(user.decrypt_sign_key(password))
        return token_for(str(user.login), sign_key, expires, role)
    except:
        return None
