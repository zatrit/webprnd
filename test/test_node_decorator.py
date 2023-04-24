from nodes import node, NodeType
from nodes.param_types import Plain, Range
from nodes.types import ParamDict
import pytest


# Тестовая функция, принимающая все возможные параметры
@node(NodeType.Seed, "testing_test", accepts_params={
    "a": Plain(5),
    "b": Plain("string!"),
    "c": Plain(False),
    "d": Range(-5, _min=-5)
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
    }) == 5


def test_valid_range():
    const_seed(params={
        "d": -4
    })


def test_invalid_type():
    with pytest.raises(ValueError):
        const_seed(params={
            "a": "5",
        })


def test_invalid_nullable_type():
    with pytest.raises(ValueError):
        const_seed(params={
            "c": "True"
        })


def test_invalid_range():
    with pytest.raises(ValueError):
        const_seed(params={
            "d": -6
        })