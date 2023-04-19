from nodes import node, NodeType
from nodes.types import ParamDict
import pytest


@node(NodeType.Seed, "testing_test", accepts_params={
    "a": (int, 1),
    "b": (str, "string!"),
    "c": (bool, False),
})
def const_seed(*, params: ParamDict) -> int:
    return params["a"]  # type: ignore


def test_valid_type():
    assert const_seed(params={
        "a": 5,
        "b": "String",
        "c": True
    }) == 5


def test_nullable_type():
    assert const_seed(params={
        "a": 5,
        "b": "String"
    }) == 5


def test_invalid_type():
    with pytest.raises(TypeError):
        const_seed(params={
            "a": "5",
            "b": "String"
        })


def test_invalid_nullable_type():
    with pytest.raises(TypeError):
        const_seed(params={
            "a": 5,
            "b": "String",
            "c": "True"
        })
