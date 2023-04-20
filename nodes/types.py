from typing import Protocol, Any, Optional
from .param_types import Param

HardParamType = int | bool | float | str
ParamType = HardParamType | Optional[HardParamType]
ParamDict = dict
ParamTypes = dict[str, Param]
OutputData = dict


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
