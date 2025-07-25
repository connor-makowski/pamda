print("\n===============\nUtil Tests:\n===============")
from pamda import pamda
from pamda.pamda_timer import pamda_timer

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


try:
    # A speical pamda timer_test to ensure that the timer works correctly
    @pamda_timer(units="ms", iterations=10)
    def my_fn(a, b):
        """
        Example function to demonstrate the use of pamda_timer.
        """
        return a + b

    my_fn.get_time_stats(1, 2)  # Example usage of the timer
except Exception as e:
    print(f"pamda_tiemer wrapper test failed: {e}")
