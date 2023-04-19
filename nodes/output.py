from .types import ParamDict, OutputData
from . import node, NodeType


@node(NodeType.Output, "json", accepts_params={
    "pretify": bool | None
})
def json(data: OutputData, *, params: ParamDict):
    print(params)
