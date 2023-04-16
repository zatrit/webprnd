from typing import Protocol, Any, Optional

HardParamType = int | bool | float | str
ParamType = HardParamType | Optional[HardParamType]
ParamDict = dict[str, ParamType]
OptParamDict = Optional[ParamDict]
OutputData = dict


class RandomFunction(Protocol):
    def __call__(self, seed: int, state: Any, *, params: OptParamDict) -> tuple[float, Any]:
        ...


class SeedFunction(Protocol):
    def __call__(self, *, params: OptParamDict) -> int:
        ...


class OutputFunction(Protocol):
    def __call__(self, data: OutputData, *, params: OptParamDict) -> None:
        ...


class WrapperFunction(Protocol):
    def __call__(self, *args, params: OptParamDict) -> Any:
        ...


Function = RandomFunction | SeedFunction | OutputFunction | WrapperFunction
