from enum import Enum


class ApiMessage(Enum):
    """Разные сообщения об ошибках для обработки их в API"""

    INVALID_OUTPUT_TYPE = "Формат выходных данных не найден"
    INVALID_NODE_TYPE = "Неверный тип ноды"
    INFINITE_LOOP = "Да, тут есть проверка на бесконечные циклы"
    SEED_INPUT = "Нельзя просто так взять, и передать данные в ноду типа seed"
    NO_OUTPUT = "В ноду типа output не было передано значение (что?)"
    NO_SEED = "Нужен хотя бы один элемент типа seed"
    WRONG_TYPE = "Неверный тип входных данных"
    NO_DATA = "Не удалось преобразовать данные"
    UNKNOWN = "Неизвестная ошибка"
    TEST = "Тест"


class ApiError(Exception):
    """Ошибка API, содержащая ApiMessage как сообщение"""

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
