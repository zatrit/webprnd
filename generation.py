from dataclasses import dataclass, field
from typing import Self
from api_error import ApiError, ApiMessage
from nodes import NodeKey, NodeType, functions
from nodes.params import fill_defaults
from nodes.types import ChainResult, Function, OutputResult, ParamDict, RandomFunction, random_params
import output_format


@dataclass
class ForwardData:
    nodes: list
    output_buffer: dict[int, list[ChainResult]]
    value: int | float | None = None
    previous: int | None = None
    route: list[int] = field(default_factory=list)


@dataclass
class Node:
    _id: int
    key: NodeKey
    to: list[int] = field(default_factory=list)
    params: ParamDict = field(default_factory=dict)

    def forward(self, data: ForwardData):
        if self._id in data.route:
            raise ApiError(ApiMessage.INFINITE_LOOP)

        if self.key._type == NodeType.Seed and data.previous != None:
            raise ApiError(ApiMessage.SEED_INPUT)

        data.route.append(self._id)
        initial_len = len(data.route)

        if self.key._type == NodeType.Output:
            if data.value == None:
                raise ApiError(ApiMessage.NO_OUTPUT)

            result = ChainResult(data.value, data.route)
            buffer = data.output_buffer[self._id] = \
                data.output_buffer.get(self._id, [])
            buffer.append(result)
            # На этом работа данной ноды окончена
            return

        value = get_seed(self) if self.key._type == NodeType.Seed \
            else get_random(self, round(data.value or 0))

        for node_id in self.to:
            data.route = data.route[:initial_len]
            node: Self = node_by_id(data.nodes, node_id)

            data = ForwardData(
                data.nodes, data.output_buffer,
                value, previous=self._id,
                route=data.route,
            )
            node.forward(data)

    # https://stackoverflow.com/a/33270983/12245612
    @classmethod
    def from_json(cls, json_dict: dict):
        key = NodeKey(NodeType(json_dict["type"]), json_dict["name"])
        return cls(_id=json_dict["id"], key=key,
                   to=json_dict["to"], params=json_dict["params"])


@dataclass
class Project:
    _format: str
    nodes: list[Node] = field(default_factory=list)

    @classmethod
    def from_json(cls: type[Self], json_dict: dict):
        return cls(
            _format=json_dict.get("format", "7z"),
            nodes=[Node.from_json(n) for n in json_dict["nodes"]])


def node_by_id(nodes: list[Node], id: int):
    return next(n for n in nodes if n._id == id)


def function_for(node: NodeKey) -> Function:
    func = functions.get(node, None)

    if not func:
        raise ApiError(ApiMessage.INVALID_NODE_TYPE)

    return func[1]


def generate_project(project: Project):
    nodes = project.nodes
    seed_nodes = [n for n in nodes if n.key._type == NodeType.Seed]
    output_buffer = {}

    if not seed_nodes:
        raise ApiError(ApiMessage.NO_SEED)

    if project._format not in output_format.formats:
        raise ApiError(ApiMessage.INVALID_OUTPUT_TYPE)

    for node in seed_nodes:
        data = ForwardData(nodes, output_buffer, node._id)
        node.forward(data)

    output = output_format.formats[project._format]()

    for _id, result in output_buffer.items():
        node = node_by_id(nodes, _id)
        func = function_for(node.key)
        output_result: OutputResult = func(
            result, params=node.params)  # type: ignore
        content, ext = output_result

        output.write(_id, ext, content)

    return output.get_content()


def get_seed(node: Node) -> int:
    return function_for(node.key)(params=node.params)  # type: ignore


def get_random(node: Node, seed: int) -> int | float:
    random: RandomFunction = function_for(node.key)  # type: ignore

    value, state = 0, None
    params: dict[str, int] = fill_defaults(node.params, random_params)

    for _ in range(params["iter"]):
        value, state = random(seed, state, params=params)

    value *= (params["max"] - params["min"])
    value += params["min"]

    if params["round"]:
        value = round(value)

    return value
