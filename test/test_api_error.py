from api_error import ApiError, ApiMessage
import pytest


def test_message():
    assert ApiMessage.TEST.value == "Тест"


def test_error():
    with pytest.raises(ApiError):
        raise ApiError(ApiMessage.NO_DATA)


def test_error_with_data():
    with pytest.raises(ApiError):
        raise ApiError(ApiMessage.NO_DATA, {"my_data": "Какое-то сообщение"})
