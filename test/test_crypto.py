from auth.crypto import token_for, verify_token
from ecdsa import SigningKey, VerifyingKey
from time import time

login, role = "zatrit", "api"
expires = int(time() + 9999999)
sign_key = SigningKey.generate()
verf_key: VerifyingKey = sign_key.verifying_key  # type: ignore


def validate_token(token: str, verify_key: VerifyingKey):
    return verify_token(token, role, int(time()), lambda _: verify_key)


def test_validation():
    token = token_for(login, sign_key, expires, role)
    assert validate_token(token, verf_key)


def test_invalidation():
    cases = [
        "FIRST:SECOND:THIRD:AAA",
        "FIRST:SECOND:THIRD:AAA:BBB",
        "FcCx_VPCl_Xd0IMZNt0fgI9pOP5U3gT1D1Jy1Ce5kfvGai9Gz1f86UZ-0eKJj6yq:AAAAAGQ26FU=:YXBp:emF0cml0",
        "NOT TOKEN AT ALL"
    ]

    for token in cases:
        assert not validate_token(token, verf_key)
