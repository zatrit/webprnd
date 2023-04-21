from .param_types import Plain
from .types import ParamDict, OutputData
from . import node, NodeType


@node(NodeType.Output, "json", accepts_params={
    "pretify": Plain(False),
})
def json(data: OutputData, *, params: ParamDict):
    print(params)


@node(NodeType.Output, "csv", accepts_params={
    "delimiter": Plain(";"),
})
def csv(data: OutputData, *, params: ParamDict):
    print(params)
