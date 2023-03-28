import auth
from hashlib import sha256

login, password_hash = b"abcdef", sha256(b"123456").digest()


def test_token():
    token = auth.token_for(login, password_hash)
    assert auth.validate(token, login, password_hash)


def test_validation():
    token = b"gAAAAABkIevPM4FnUHng5mSjUye8FPTcqNm4mtaDqx7Rq8EnX1TQwEO8LRhqP15aX-avvNo626VEWMXMUIN9zZZkYoecxmkWR87WEtC7HYB6ZWMF6tvJwusSJVcTV2moBK4gXq93V-mY"
    assert auth.validate(token, login, password_hash)


def test_invalidation1():
    token = b'NOT A VALID TOKEN'
    assert not auth.validate(token, login, password_hash)


def test_invalidation2():
    token = auth.token_for(login, password_hash)
    assert not auth.validate(token, b"another login", password_hash)
