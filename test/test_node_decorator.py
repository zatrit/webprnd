from nodes import ParamDict, node, NodeType
import pytest


@node(NodeType.Seed, "testing_test", accepts_params={
    "a": int,
    "b": str,
    "c": bool | None,
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
    const_seed(params={
        "a": 5,
        "b": "String"
    })


def test_missing():
    with pytest.raises(ValueError):
        const_seed(params={
            "a": 5
        })


def test_invalid_type():
    with pytest.raises(ValueError):
        const_seed(params={
            "a": "5",
            "b": "String"
        })


def test_invalid_nullable_type():
    with pytest.raises(ValueError):
        const_seed(params={
            "a": 5,
            "b": "String",
            "c": "True"
        })
