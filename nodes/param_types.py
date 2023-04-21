from typing import Any, Protocol, TypeVar, Generic
from sys import maxsize

# Сокр. Param type
PT = TypeVar("PT")
# Сокр. Plain param type
PPT = TypeVar("PPT", str, int, float, bool)
# Сокр. Range param type
RPT = TypeVar("RPT", int, float)


class Param(Protocol, Generic[PT]):
    default: PT

    def validate(self, value: PT) -> bool:
        ...

    def serialize(self) -> dict[str, Any]:
        ...


# Число, строка, булевое значение и т.д.
class Plain(Param[PPT], Generic[PPT]):
    def __init__(self, default: PPT, _type: type[PPT] | None = None) -> None:
        super().__init__()

        self.default = default
        self._type = _type or type(default)

    def validate(self, value: Any) -> bool:
        return isinstance(value, self._type)

    def serialize(self) -> dict[str, Any]:
        return {
            "type": self._type.__name__,
            "default": self.default
        }


# Число из определённого диапазона
class Range(Plain[RPT], Generic[RPT]):
    def __init__(self, default: RPT, _type: type[RPT] | None = None, _min=-maxsize, _max=maxsize) -> None:
        super().__init__(default, _type)
        self.min, self.max = _min, _max

    def validate(self, value: Any) -> bool:
        return isinstance(value, self._type) \
            and self.min <= value <= self.max  # type: ignore

    def serialize(self) -> dict[str, Any]:
        return super().serialize() | {"type": "range", "min": self.min, "max": self.max}
