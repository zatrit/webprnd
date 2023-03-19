from sqlalchemy import Column, Integer
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    login = Column(Integer, primary_key=True,
                   comment="Хэш логина пользователя")
    password = Column(Integer,
                      comment="Хэш пароля пользователя")
