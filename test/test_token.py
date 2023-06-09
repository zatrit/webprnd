from time import sleep
from data.db_session import create_session, global_init
from auth.token import validate_token, generate_token
from data.users import User

# База данных находится в памяти, так как я не хочу
# выполнять тесты на главной базе и не знаю, куда
# сохранять тестовую
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


def create_token(password: str, expires: int):
    with create_session() as db_sess:
        user: User | None = db_sess.query(User).first()
        return generate_token(user, password, expires, role)


def test_validation():
    token = create_token(password, 0)
    assert validate_token(token, [role])


def test_expiration():
    token = create_token(password, 1)
    sleep(2)
    assert not validate_token(token,  [role])


def test_wrong_password():
    token = create_token("wrong password", 0)
    assert not validate_token(token,  [role])


def test_role_invalidation():
    token = create_token(password, 0)
    assert not validate_token(token, ["invalid role"])


def test_role_and_token_invalidation():
    for token in invalid_cases:
        assert not validate_token(token,  [role])
