from enum import Enum
from functools import wraps
from typing import Optional, Callable, Any


class NodeType(Enum):
    Seed = "seed"
    Random = "random"
    Output = "output"


HardParamType = int | bool | float | str
ParamType = HardParamType | Optional[HardParamType]
ParamDict = dict[str, ParamType]

RandomFunction = Callable[[int, Any], tuple[float, Any]]
SeedFunction = Callable[[], int]


def node(node_type: NodeType, name: str, accepts_params: dict[str, type[ParamType]] = {}):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, params: Optional[ParamDict], **kwargs, ):
            # Тут идёт явная проверка типов
            # По сути является контрактом, гарантирующим,
            # что передаваемые параметры подходят под accepts_params
            if params:
                for key, value in params.items():
                    if key not in accepts_params:
                        raise ValueError("Неизвестный параметр " + key)

                for key, value in accepts_params.items():
                    if not isinstance(params.get(key, None), value):
                        raise ValueError(
                            "Неверный тип или отсутсвующий параметр " + key)
            elif accepts_params:
                raise ValueError("Отсутствует поле params")

            return fn(*args, **kwargs, params=params)
        return wrapper
    return decorator
