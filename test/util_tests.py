import pytest
from pamda import pamda
from pamda.pamda_timer import pamda_timer


def test_read_csv_no_cast():
    data = pamda.read_csv("test/test_data/data.csv", cast_items=False)
    assert data == [{"a": "1", "b": "true", "c": "1.5", "d": "abc"}]


def test_read_csv_cast_items():
    data = pamda.read_csv("test/test_data/data.csv")
    assert data == [{"a": 1, "b": True, "c": 1.5, "d": "abc"}]


def test_read_csv_cast_dict():
    data = pamda.read_csv(
        "test/test_data/data.csv",
        cast_dict={"a": int, "b": bool, "c": float, "d": str},
    )
    assert data == [{"a": 1, "b": True, "c": 1.5, "d": "abc"}]


def test_read_csv_return_type_list_of_dicts():
    data = pamda.read_csv(
        "test/test_data/data.csv",
        cast_items=False,
        return_type="list_of_dicts",
    )
    assert data == [{"a": "1", "b": "true", "c": "1.5", "d": "abc"}]


def test_read_csv_return_type_dict_of_lists():
    data = pamda.read_csv(
        "test/test_data/data.csv", return_type="dict_of_lists"
    )
    assert data == {"a": [1], "b": [True], "c": [1.5], "d": ["abc"]}


def test_read_csv_return_type_list_of_row_lists():
    data = pamda.read_csv(
        "test/test_data/data.csv", return_type="list_of_row_lists"
    )
    assert data == [["a", "b", "c", "d"], [1, True, 1.5, "abc"]]


def test_read_csv_return_type_list_of_col_lists():
    data = pamda.read_csv(
        "test/test_data/data.csv", return_type="list_of_col_lists"
    )
    assert data == [["a", 1], ["b", True], ["c", 1.5], ["d", "abc"]]


def test_pamda_timer_decorator():
    @pamda_timer(units="ms", iterations=10)
    def my_fn(a, b):
        return a + b

    my_fn.get_time_stats(1, 2)
