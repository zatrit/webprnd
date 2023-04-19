from typing import Any
from .types import ParamDict
from . import node, NodeType


@node(NodeType.Random, "linear_congruential",
      accepts_params={"m": (int, 0x7FFFFFFF), "a": (int, 1664525), "c": (int, 1013904223)})
def linear_congruential(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    result: int = (state * params["a"] + params["c"]) & params["m"]
    return result / params["m"], result


@node(NodeType.Random, "quadratic_congruential",
      accepts_params={"m": (int, 0x7FFFFFFF), "a": (int, 1664525),
                      "c": (int, 1013904223), "d": (int, 1664524)})
def quadratic_congruential(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    result: int = (state ** 2 * params["d"] + params["a"] *
                   state + params["c"]) & params["m"]
    return result / params["m"], result


@node(NodeType.Random, "python")
def python_random(seed: int, state: Any, *, params: ParamDict) -> tuple[float, int]:
    from random import Random
    if not state:
        state = Random(seed)
    return state.random(), state


@node(NodeType.Random, "lfsr_xorshift", accepts_params={"m": (int, 0x7FFFFFFF)})
def lfsr_xorshift(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    state ^= state >> 7
    state ^= state << 9
    state ^= state >> 13
    state &= params["m"]
    return state / params["m"], state


@node(NodeType.Random, "blum_blum_shub", accepts_params={"p": (int, 1664543), "q": (int, 1013904223)})
def blum_blum_shub(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    m = params["p"] * params["q"]
    state = (state ** 2) % m
    return state / m, state
