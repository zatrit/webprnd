import auth

login, password = b"abcdef", b"123456"


def test_token():
    token = auth.token_for(login, password)
    assert auth.validate(token, login, password)


def test_validation():
    token = b"gAAAAABkFuwRX1wYYxSQ5_izPwcR5aH8f0sVgDkxHJM0FYN9tCx7g32p0Qo-1tptEqbbPplFKLcrg07B3lM8keSe5qu-JjhQ5fb8o_WFDESIwz3ehg0mWZ3sImJ4Gwhb02Su5GxGySbM"
    assert auth.validate(token, login, password)


def test_invalidation1():
    token = b'NOT A VALID TOKEN'
    assert not auth.validate(token, login, password)


def test_invalidation2():
    token = auth.token_for(login, password)
    assert not auth.validate(token, b"another login", password)
