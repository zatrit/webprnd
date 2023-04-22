from dataclasses import dataclass
from typing import Protocol, Any
from .param_types import Param, Plain, Range

ParamDict = dict
ParamTypes = dict[str, Param]
random_params: ParamTypes = {
    "iter": Range(1, _min=1, _max=50),
    "max": Plain(1000),
    "min": Plain(-1000),
    "round": Plain(True)
}
# Содержит контент и расширение
OutputResult = tuple[str | bytes, str]


@dataclass
class ChainResult:
    value: int | float
    passed_nodes: list[int]


class RandomFunction(Protocol):
    def __call__(self, seed: int, state: Any, *, params: ParamDict) -> tuple[float, Any]:
        ...


class SeedFunction(Protocol):
    def __call__(self, *, params: ParamDict) -> int:
        ...


class OutputFunction(Protocol):
    def __call__(self, result:  list[ChainResult], *, params: ParamDict) -> OutputResult:
        ...


class WrapperFunction(Protocol):
    def __call__(self, *args, params: ParamDict) -> Any:
        ...


Function = RandomFunction | SeedFunction | OutputFunction
