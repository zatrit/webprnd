from .types import ParamDict, OutputData
from . import node, NodeType


@node(NodeType.Output, "json", accepts_params={
    "pretify": (bool, False)
})
def json(data: OutputData, *, params: ParamDict):
    print(params)


@node(NodeType.Output, "csv")
def csv(data: OutputData, *, params: ParamDict):
    print(params)
