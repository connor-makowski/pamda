print("\n===============\nUtil Tests:\n===============")
from pamda import pamda

data = pamda.read_csv("test_data/data.csv", cast_items=False)
if data != [{"a": "1", "b": "true", "c": "1.5", "d": "abc"}]:
    print("read_csv (no inputs) failed")

data = pamda.read_csv("test_data/data.csv")
if data != [{"a": 1, "b": True, "c": 1.5, "d": "abc"}]:
    print("read_csv cast_items failed")

data = pamda.read_csv(
    "test_data/data.csv", cast_dict={"a": int, "b": bool, "c": float, "d": str}
)
if data != [{"a": 1, "b": True, "c": 1.5, "d": "abc"}]:
    print("read_csv cast_dict failed")

data = pamda.read_csv(
    "test_data/data.csv", cast_items=False, return_type="list_of_dicts"
)
if data != [{"a": "1", "b": "true", "c": "1.5", "d": "abc"}]:
    print("read_csv (no inputs) failed")

data = pamda.read_csv("test_data/data.csv", return_type="dict_of_lists")
if data != {"a": [1], "b": [True], "c": [1.5], "d": ["abc"]}:
    print("read_csv return_type=dict_of_lists failed")

data = pamda.read_csv("test_data/data.csv", return_type="list_of_row_lists")
if data != [["a", "b", "c", "d"], [1, True, 1.5, "abc"]]:
    print("read_csv return_type=list_of_row_lists failed")

data = pamda.read_csv("test_data/data.csv", return_type="list_of_col_lists")
if data != [["a", 1], ["b", True], ["c", 1.5], ["d", "abc"]]:
    print("read_csv return_type=list_of_col_lists failed")
