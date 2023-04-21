from auth.crypto import token_for, verify_token
from ecdsa import SigningKey, VerifyingKey
from time import time

login, role = "zatrit", "api"
expires = int(time() + 9999999)
sign_key = SigningKey.generate()
verf_key: VerifyingKey = sign_key.verifying_key  # type: ignore

# Случаи, когда 
invalid_cases = [
    "FIRST:SECOND:THIRD:AAA",
    "FIRST:SECOND:THIRD:AAA:BBB",
    "FcCx_VPCl_Xd0IMZNt0fgI9pOP5U3gT1D1Jy1Ce5kfvGai9Gz1f86UZ-0eKJj6yq:AAAAAGQ26FU=:YXBp:emF0cml0",
    "NOT TOKEN AT ALL",
]


def validate_token(token: str, role: list[str], verify_key: VerifyingKey):
    # Каким-то образом, тесты проходили даже когда role был передан
    # как строка. Оператор in - забавная вещь
    return verify_token(token, role, int(time()), lambda _: verify_key)


def test_validation():
    token = token_for(login, sign_key, expires, role)
    assert validate_token(token, [role], verf_key)


def test_invalidation():
    for token in invalid_cases:
        assert not validate_token(token, [role], verf_key)


def test_role_invalidation():
    token = token_for(login, sign_key, expires, role)
    assert not validate_token(token, ["invalid role"], verf_key)


def test_role_and_token_invalidation():
    for token in invalid_cases:
        assert not validate_token(token, ["invalid role"], verf_key)
