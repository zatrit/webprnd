from .param_types import Plain
from .types import ParamDict
from . import node, NodeType


@node(NodeType.Seed, "const", accepts_params={"value": Plain(5)})
def const(*, params: ParamDict) -> int:
    return params["value"]


@node(NodeType.Seed, "time")
def time_ns(*, params: ParamDict) -> int:
    from time import time_ns
    return time_ns()


@node(NodeType.Seed, "urandom", accepts_params={"n_bytes": Plain(8)})
def urandom(*, params: ParamDict) -> int:
    from os import urandom as _urandom
    return int.from_bytes(_urandom(params["n_bytes"]))
