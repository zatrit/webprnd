from abc import abstractmethod
from enum import StrEnum


class ApiMessage(StrEnum):
    INFINITE_LOOP = "Да, тут есть проверка на бесконечные циклы"
    SEED_INPUT = "Нельзя просто так взять, и передать данные в ноду типа seed"
    NO_OUTPUT = "В ноду типа output не было передано значение (что?)"
    NO_SEED = "Нужен хотя бы один элемент типа seed"
    WRONG_TYPE = "Неверный тип входных данных"
    NO_DATA = "Не удалось преобразовать данные"


class ApiError(Exception):
    error: ApiMessage
    data: dict[str, str]

    def __init__(self, message: ApiMessage, data: dict[str, str] | None = None) -> None:
        self.data = data or {}
        self.message = message

    def json(self) -> dict[str, str]:
        return {
            "message": self.message.value,
            "error:": self.message.name,
        } | self.data
