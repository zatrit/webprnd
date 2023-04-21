from dataclasses import dataclass
from enum import Enum
from functools import wraps
from .types import Function, ParamDict, ParamTypes, WrapperFunction, random_params


class NodeType(Enum):
    Seed = "seed"
    Random = "random"
    Output = "output"


@dataclass(repr=False, unsafe_hash=True)
class NodeKey:
    node_type: NodeType
    name: str


registry: dict[NodeKey, tuple[ParamTypes, Function | WrapperFunction]] = {}


def node(node_type: NodeType, name: str, accepts_params: ParamTypes | None = None):
    if accepts_params == None:
        accepts_params = {}

    if node_type == NodeType.Random:
        accepts_params |= random_params

    def decorator(fn: Function):
        @wraps(fn)
        def wrapper(*args, params: ParamDict):
            # Тут идёт явная проверка типов
            # По сути является контрактом, гарантирующим,
            # что передаваемые параметры подходят под accepts_params
            forward_params = {}

            for key, _ in (params or {}).items():
                if key not in accepts_params:
                    raise ValueError("Неизвестный параметр " + key)

            for key, param in accepts_params.items():
                value = params.get(key, param.default)
                if not param.validate(value):
                    raise ValueError("Неверный тип или значение " + key)
                forward_params[key] = value

            return fn(*args, params=forward_params)
        key = NodeKey(node_type, name)
        registry[key] = (accepts_params, wrapper)

        return wrapper
    return decorator


def init_nodes():
    from . import seed, random, output
