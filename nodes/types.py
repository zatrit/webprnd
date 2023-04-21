from typing import Protocol, Any
from .param_types import Param, Range

ParamDict = dict
ParamTypes = dict[str, Param]
OutputData = dict
random_params: ParamTypes = {"iter": Range(1, _min=1, _max=50)}


class RandomFunction(Protocol):
    def __call__(self, seed: int, state: Any, *, params: ParamDict) -> tuple[float, Any]:
        ...


class SeedFunction(Protocol):
    def __call__(self, *, params: ParamDict) -> int:
        ...


class OutputFunction(Protocol):
    def __call__(self, data: OutputData, *, params: ParamDict) -> None:
        ...


class WrapperFunction(Protocol):
    def __call__(self, *args, params: ParamDict) -> Any:
        ...


Function = RandomFunction | SeedFunction | OutputFunction
