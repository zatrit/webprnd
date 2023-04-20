from typing import Any, Protocol, TypeVar, Generic

# Сокр. Param type
PT = TypeVar("PT")
# Сокр. Plain param type
PPT = TypeVar("PPT", str, int, float, bool)


class Param(Protocol, Generic[PT]):
    default: PT

    def validate(self, value: PT) -> bool:
        ...

    def serialize(self) -> dict[str, Any]:
        ...


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
