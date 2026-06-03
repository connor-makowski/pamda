import pytest
from pamda import pamda


def test_curryTyped_valid():
    @pamda.curryTyped
    def my_fn(a: int, b: list[str]) -> str:
        return str(a) + b[0]

    assert my_fn(1)(["2"]) == "12"


def test_curryTyped_invalid_list_item_type():
    @pamda.curryTyped
    def my_fn(a: int, b: list[str]) -> str:
        return str(a) + b[0]

    with pytest.raises(Exception):
        my_fn(1)([2])


def test_curryTyped_invalid_arg_type():
    @pamda.curryTyped
    def my_fn(a: int, b: list[str]) -> str:
        return str(a) + b[0]

    with pytest.raises(Exception):
        my_fn(1)(2)
