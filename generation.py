from dataclasses import dataclass, field
from typing import Self
from api_error import ApiError, ApiMessage
from nodes import NodeKey, NodeType
from nodes.types import ParamDict


@dataclass
class ChainResult:
    value: int
    passed_nodes: list[int]


@dataclass
class ForwardData:
    nodes: list
    output_buffer: dict[int, ChainResult]
    value: int | None = None
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

        if self.key._type == NodeType.Output:
            if data.value == None:
                raise ApiError(ApiMessage.NO_OUTPUT)

            data.output_buffer[self._id] = ChainResult(data.value, data.route)

        data.route.append(self._id)
        initial_len = len(data.route)

        for node_id in self.to:
            data.route = data.route[:initial_len]
            node: Self = next(n for n in data.nodes if n._id == node_id)

            data = ForwardData(
                data.nodes, value=0,
                previous=self._id,
                route=data.route,
                output_buffer=data.output_buffer
            )
            node.forward(data)

    # https://stackoverflow.com/a/33270983/12245612
    @classmethod
    def from_json(cls, json_dict: dict):
        key = NodeKey(NodeType(json_dict["type"]), json_dict["name"])
        return cls(_id=json_dict["id"], key=key, to=json_dict["to"])


@dataclass
class Project:
    nodes: list[Node] = field(default_factory=list)

    @classmethod
    def from_json(cls: type[Self], json_dict: dict):
        return cls(nodes=[Node.from_json(n) for n in json_dict["nodes"]])


def generate_project(project: Project):
    nodes = project.nodes
    seed_nodes = [n for n in nodes if n.key._type == NodeType.Seed]
    output_buffer = {}

    if not seed_nodes:
        raise ApiError(ApiMessage.NO_SEED)

    for node in seed_nodes:
        data = ForwardData(nodes, output_buffer, node._id)
        node.forward(data)

    print(output_buffer)
