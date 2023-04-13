from time import sleep
from data.db_session import create_session, global_init
from auth.token import validate_token, generate_token
from data.users import User

global_init(":memory:")
with create_session() as db_sess:
    password, role = "123456", "api"
    user = User.new("zatrit", password)

    db_sess.add(user)
    db_sess.commit()

invalid_cases = [
    "FIRST:SECOND:THIRD:AAA",
    "FIRST:SECOND:THIRD:AAA:BBB",
    "FcCx_VPCl_Xd0IMZNt0fgI9pOP5U3gT1D1Jy1Ce5kfvGai9Gz1f86UZ-0eKJj6yq:AAAAAGQ26FU=:YXBp:emF0cml0",
    "NOT TOKEN AT ALL",
]


def test_validation():
    with create_session() as db_sess:
        user = db_sess.query(User).first()
        token = generate_token(user, password, 0, role)
    assert validate_token(token, role)


def test_expiration():
    with create_session() as db_sess:
        user = db_sess.query(User).first()
        token = generate_token(user, password, 1, role)
    sleep(2)
    assert not validate_token(token, role)


def test_wrong_password():
    with create_session() as db_sess:
        user = db_sess.query(User).first()
        token = generate_token(user, "wrong password", 0, role)
    assert not validate_token(token, role)


def test_role_invalidation():
    with create_session() as db_sess:
        user = db_sess.query(User).first()
        token = generate_token(user, password, 0, role)
    assert not validate_token(token, "invalid role")


def test_role_and_token_invalidation():
    for token in invalid_cases:
        assert not validate_token(token, role)
