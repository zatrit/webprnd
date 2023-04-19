from typing import Protocol, Any, Optional

HardParamType = int | bool | float | str
ParamType = HardParamType | Optional[HardParamType]
ParamDict = dict
ParamTypes = dict[str, tuple[type[ParamType], Any]]
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
