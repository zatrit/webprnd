from typing import Any

from .param_types import Plain
from .types import ParamTypes, ParamDict
from . import node, NodeType

modulo_params: ParamTypes = {"m": Plain(0x7FFFFFFF)}
lcg_params: ParamTypes = modulo_params | \
    {"a": Plain(1664525), "c": Plain(1013904223)}
ccg_params: ParamTypes = lcg_params | {"d": Plain(1664524)}


@node(NodeType.Random, "linear_congruential", accepts_params=lcg_params)
def linear_congruential(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    result: int = (state * params["a"] + params["c"]) & params["m"]
    return result / params["m"], result


@node(NodeType.Random, "quadratic_congruential", accepts_params=ccg_params)
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


@node(NodeType.Random, "lfsr_xorshift", accepts_params=modulo_params)
def lfsr_xorshift(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    state ^= state >> 7
    state ^= state << 9
    state ^= state >> 13
    state &= params["m"]
    return state / params["m"], state


@node(NodeType.Random, "blum_blum_shub",
      accepts_params={"p": Plain(1664543), "q": Plain(1013904223)})
def blum_blum_shub(seed: int, state: int, *, params: ParamDict) -> tuple[float, int]:
    if not state:
        state = seed
    m = params["p"] * params["q"]
    state = (state ** 2) % m
    return state / m, state
