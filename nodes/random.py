from typing import Any
from .types import ParamDict
from . import node, NodeType


@node(NodeType.Random, "linear_congruential",
      accepts_params={"m": int, "a": int, "c": int})
def linear_congruential(seed: int, state: Any, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    result: int = (state * params["a"] + params["c"]) & params["m"]
    return result / params["m"], result
