from dataclasses import dataclass
from enum import Enum
from functools import wraps

from nodes.params import fill_defaults
from .types import Function, ParamDict, ParamTypes, WrapperFunction, random_params


class NodeType(Enum):
    Seed = "seed"
    Random = "random"
    Output = "output"


@dataclass(repr=False, unsafe_hash=True)
class NodeKey:
    _type: NodeType
    name: str

    def __repr__(self) -> str:
        return self._type.value + "." + self.name

    __str__ = __repr__


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

            return fn(*args, params=fill_defaults(params, accepts_params))
        key = NodeKey(node_type, name)
        registry[key] = (accepts_params, wrapper)

        return wrapper
    return decorator


def init_nodes():
    from . import seed, random, output
