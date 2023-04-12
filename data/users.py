from sqlalchemy import Column, String, BINARY
from ecdsa import SigningKey, VerifyingKey
from auth.crypto import fernet_for
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = "users"

    login = Column(String, primary_key=True,
                   comment="Логин пользователя")
    sign_key = Column(BINARY, comment="Зашифрованный " +
                      "паролем ключ для подписи токена")
    verify_key = Column(BINARY, comment="Ключ для " +
                        "проверки подписи токена")
    password_hash = Column(String, comment="Хэш пароля")

    @staticmethod
    def new(login: str, password: str):
        fernet = fernet_for(password)
        sign_key: SigningKey = SigningKey.generate()
        verf_key: VerifyingKey = sign_key.verifying_key  # type: ignore
        sk: bytes = fernet.encrypt(sign_key.to_string())
        vk: bytes = verf_key.to_string()

        return User(login=login, sign_key=sk, verify_key=vk,
                    password_hash=generate_password_hash(password))

    def decrypt_sign_key(self, password: str) -> bytes | None:
        try:
            fernet = fernet_for(password)
            return fernet.decrypt(self.sign_key)  # type: ignore
        except:
            return None

    def check_password(self, password: str) -> bool:
        r = check_password_hash(self.password_hash, password)  # type: ignore
        return r
