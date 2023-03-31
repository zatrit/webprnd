from sqlalchemy import Column, BINARY
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    login = Column(BINARY, primary_key=True,
                   comment="Хэш логина пользователя")
    password = Column(BINARY,
                      comment="Хэш пароля пользователя")

    @staticmethod
    def new(login: str, password: str):
        from hashlib import sha256

        login, password = (sha256(s.encode()).digest() for s in (login, password)) # type: ignore

        return User(login=login, password=password)
