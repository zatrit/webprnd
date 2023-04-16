from dataclasses import dataclass
from enum import Enum
from functools import wraps
from .types import Function, ParamType, OptParamDict


class NodeType(Enum):
    Seed = "seed"
    Random = "random"
    Output = "output"


@dataclass(repr=False, unsafe_hash=True)
class NodeKey:
    node_type: NodeType
    name: str


registry: dict[NodeKey, Function] = {}


def node(node_type: NodeType, name: str, accepts_params: dict[str, type[ParamType]] = {}):
    def decorator(fn: Function):
        @wraps(fn)
        def wrapper(*args, params: OptParamDict):
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

            return fn(*args, params=params)
        key = NodeKey(node_type, name)
        registry[key] = wrapper

        return wrapper
    return decorator
