from io import StringIO
from .param_types import Plain
from .types import OutputResult, ParamDict, ChainResult
from . import node, NodeType


@node(NodeType.Output, "json", accepts_params={
    "pretify": Plain(False),
})
def json(result: list[ChainResult], *, params: ParamDict) -> OutputResult:
    from ujson import dumps

    dicts = [o.__dict__ for o in result]
    pretify_kwargs = {"indent": 2, "sort_keys": True}
    kwargs = pretify_kwargs if params["pretify"] else {}
    content = dumps(dicts, **kwargs)
    return content, "json"


@ node(NodeType.Output, "csv", accepts_params={
    "delimiter": Plain(";"),
    "qoute": Plain('"'),
    "header": Plain(True),
})
def csv(result: list[ChainResult], *, params: ParamDict) -> OutputResult:
    import csv
    with StringIO() as io:
        writer = csv.writer(
            io, delimiter=params["delimiter"], quotechar=params["qoute"],
            quoting=csv.QUOTE_ALL)
        writer.writerow(("result", "passed nodes"))
        for res in result:
            writer.writerow((res.value, str(res.passed_nodes)))
        return io.getvalue(), "csv"
