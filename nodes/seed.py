from .types import ParamDict
from . import node, NodeType


@node(NodeType.Seed, "const", accepts_params={
    "value": int
})
def json(*, params: ParamDict):
    return params["value"]
