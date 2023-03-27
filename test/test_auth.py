import auth
from hashlib import sha256

login, password_hash = b"abcdef", sha256(b"123456").digest()


def test_token():
    token = auth.token_for(login, password_hash)
    assert auth.validate(token, login, password_hash)


def test_validation():
    token = b"gAAAAABkIWRruyMEU5DnZq_VVzWU-TxIRQiyyRo07vLeQcZNc8Xz2DbNoz8J4sWIpYVQQ4501I5dGnu01MJ80iLFM0ryeUcYe19AJ48HSwmjYUs09ztjyhkH42qq-glkS-NfE0SHPzOX"
    assert auth.validate(token, login, password_hash)


def test_invalidation1():
    token = b'NOT A VALID TOKEN'
    assert not auth.validate(token, login, password_hash)


def test_invalidation2():
    token = auth.token_for(login, password_hash)
    assert not auth.validate(token, b"another login", password_hash)
