import pytest
from pamda import pamda


def test_accumulate():
    out = pamda.accumulate(
        fn=pamda.add, initial_accumulator=0, data=[1, 2, 3, 4]
    )
    assert out == [1, 3, 6, 10]


def test_add():
    assert pamda.add(1, 2) == 3


def test_adjust():
    assert pamda.adjust(index=1, fn=pamda.inc, data=[1, 5, 9]) == [1, 6, 9]


def test_assocPath():
    data = {"a": {"b": 1}}
    assert pamda.assocPath(path=["a", "c"], value=3, data=data) == {
        "a": {"b": 1, "c": 3}
    }

    data = {("a", "b"): 1}
    assert pamda.assocPath(path=("a", "c"), value=3, data=data) == {
        ("a", "b"): 1,
        ("a", "c"): 3,
    }

    data = {"a": {"b": 1}}
    assert pamda.assocPath(path=["a", "b", "c"], value=3, data=data) == {
        "a": {"b": {"c": 3}}
    }

    data = {"a": ["b", "c", "d"]}
    assert pamda.assocPath(path=["a", 1], value="e", data=data) == {
        "a": ["b", "e", "d"]
    }

    data = {"a": [{"b": 1}, {"b": 2}]}
    assert pamda.assocPath(path=["a", 1, "b"], value=3, data=data) == {
        "a": [{"b": 1}, {"b": 3}]
    }


def test_assocPathComplex():
    data = {"a": {"b": 1}}
    out = pamda.assocPathComplex(
        default=[2], default_fn=lambda x: x + [1], path=["a", "c"], data=data
    )
    assert out == {"a": {"b": 1, "c": [2, 1]}}


def test_clamp():
    assert pamda.clamp(1, 10, 11) == 10
    assert pamda.clamp(1, 10, 0) == 1


def test_curry():
    def add(a, b):
        return a + b

    curried_add = pamda.curry(add)
    assert curried_add(1)(2) == 3


def test_curryTyped():
    def add(a: int, b: int) -> int:
        return a + b

    curry_typed_add = pamda.curryTyped(add)
    assert curry_typed_add(1)(2) == 3

    with pytest.raises(Exception):
        curry_typed_add(1.5)(2.5)


def test_dec():
    assert pamda.dec(1) == 0


def test_difference():
    assert pamda.difference([1, 2, 3], [2, 3, 4]) == [1]


def test_dissocPath():
    data = {"a": {"b": 1, "c": 2}}
    assert pamda.dissocPath(path=["a", "c"], data=data) == {"a": {"b": 1}}


def test_flatten():
    assert pamda.flatten([1, 2, [3, [4]]]) == [1, 2, 3, 4]
    assert pamda.flatten(data=[["a", "b"], [1, 2]]) == ["a", "b", 1, 2]


def test_flip():
    def doubleA(a, b):
        return a * 2

    assert pamda.flip(doubleA)(1, 2) == 4


def test_getArity():
    def add(a, b):
        return a + b

    assert pamda.getArity(add) == 2


def test_groupBy():
    def getGrade(item):
        score = item["score"]
        if score > 90:
            return "A"
        elif score > 80:
            return "B"
        elif score > 70:
            return "C"
        elif score > 60:
            return "D"
        else:
            return "F"

    data = [
        {"name": "Connor", "score": 75},
        {"name": "Fred", "score": 79},
        {"name": "Joe", "score": 84},
    ]
    expected = {
        "B": [{"name": "Joe", "score": 84}],
        "C": [
            {"name": "Connor", "score": 75},
            {"name": "Fred", "score": 79},
        ],
    }
    assert pamda.groupBy(getGrade, data) == expected


def test_groupKeys():
    data = [
        {"color": "red", "size": 9, "shape": "ball"},
        {"color": "red", "size": 10, "shape": "ball"},
        {"color": "green", "size": 11, "shape": "ball"},
        {"color": "green", "size": 12, "shape": "square"},
    ]
    expected = [
        [
            {"color": "red", "size": 9, "shape": "ball"},
            {"color": "red", "size": 10, "shape": "ball"},
        ],
        [{"color": "green", "size": 11, "shape": "ball"}],
        [{"color": "green", "size": 12, "shape": "square"}],
    ]
    assert pamda.groupKeys(["color", "shape"], data) == expected


def test_groupWith():
    def areEqual(a, b):
        return a == b

    data = [1, 2, 3, 1, 1, 2, 2, 3, 3, 3]
    expected = [[1], [2], [3], [1, 1], [2, 2], [3, 3, 3]]
    assert pamda.groupWith(areEqual, data) == expected


def test_hardRound():
    assert pamda.hardRound(2, 1.2345) == 1.23
    assert pamda.hardRound(0, 1.2345) == 1


def test_hasPath():
    data = {"a": {"b": 1}}
    assert pamda.hasPath(path=["a", "b"], data=data)
    assert not pamda.hasPath(path=["a", "c"], data=data)


def test_head():
    assert pamda.head([1, 2, 3]) == 1
    assert pamda.head("abc") == "a"


def test_inc():
    assert pamda.inc(1) == 2


def test_intersection():
    assert pamda.intersection([1, 2, 3], [2, 3, 4]) == [2, 3]


def test_map():
    assert pamda.map(pamda.inc, [1, 2, 3]) == [2, 3, 4]


def test_mean():
    assert pamda.mean([1, 2, 3]) == 2


def test_median():
    assert pamda.median([1, 2, 3]) == 2


def test_mergeDeep():
    data1 = {"a": {"b": 1, "c": 2}}
    data2 = {"a": {"b": 3, "d": 4}}
    expected = {"a": {"b": 3, "c": 2, "d": 4}}
    assert pamda.mergeDeep(update_data=data2, data=data1) == expected


def test_nest():
    data = [
        {"x_1": "a", "x_2": "b", "output": "c"},
        {"x_1": "a", "x_2": "b", "output": "d"},
        {"x_1": "a", "x_2": "e", "output": "f"},
    ]
    expected = {"a": {"b": ["c", "d"], "e": ["f"]}}
    out = pamda.nest(path_keys=["x_1", "x_2"], value_key="output", data=data)
    assert out == expected


def test_nestItem():
    data = [
        {"x_1": "a", "x_2": "b"},
        {"x_1": "a", "x_2": "b"},
        {"x_1": "a", "x_2": "e"},
    ]
    expected = {
        "a": {
            "b": [{"x_1": "a", "x_2": "b"}, {"x_1": "a", "x_2": "b"}],
            "e": [{"x_1": "a", "x_2": "e"}],
        }
    }
    assert pamda.nestItem(path_keys=["x_1", "x_2"], data=data) == expected


def test_path():
    data = {"a": {"b": 1}, "c": [2]}
    assert pamda.path(path=["a", "b"], data=data) == 1
    assert pamda.path(path=["c", 0], data=data) == 2


def test_pathOr():
    data = {"a": {"b": 1}, "c": [2]}
    assert pamda.pathOr(default=2, path=["a", "b"], data=data) == 1
    assert pamda.pathOr(default=2, path=["a", "c"], data=data) == 2
    assert pamda.pathOr(default=3, path=["c", 0], data=data) == 2
    assert pamda.pathOr(default=3, path=["c", 1], data=data) == 3


def test_pipe():
    def add(a, b):
        return a + b

    def double(a):
        return a * 2

    assert pamda.pipe(fns=[add, double], args=(1, 2), kwargs={}) == 6

    data = ["abc", "def"]
    assert (
        pamda.pipe(fns=[pamda.head, pamda.tail], args=(data,), kwargs={}) == "c"
    )
    assert (
        pamda.pipe(fns=[pamda.head, pamda.tail], args=(), kwargs={"data": data})
        == "c"
    )

    data = {"a": {"b": "c"}}
    curriedPath = pamda.curry(pamda.path)
    assert (
        pamda.pipe(fns=[curriedPath(["a", "b"])], args=(data,), kwargs={})
        == "c"
    )


def test_pivot():
    data = [
        {"a": "a1", "b": "b1", "c": "c1"},
        {"a": "a2", "b": "b2", "c": "c2"},
    ]
    assert pamda.pivot(data) == {
        "a": ["a1", "a2"],
        "b": ["b1", "b2"],
        "c": ["c1", "c2"],
    }

    data = {"a": ["a1", "a2"], "b": ["b1", "b2"], "c": ["c1", "c2"]}
    assert pamda.pivot(data) == [
        {"a": "a1", "b": "b1", "c": "c1"},
        {"a": "a2", "b": "b2", "c": "c2"},
    ]


def test_pluck():
    data = [{"a": {"b": 1, "c": "d"}}, {"a": {"b": 2, "c": "e"}}]
    assert pamda.pluck(path=["a", "b"], data=data) == [1, 2]


def test_pluckIf():
    data = [{"a": {"b": 1, "c": "d"}}, {"a": {"b": 2, "c": "e"}}]
    assert pamda.pluckIf(
        fn=lambda x: x["a"]["b"] == 1, path=["a", "c"], data=data
    ) == ["d"]


def test_project():
    data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
    assert pamda.project(keys=["a", "c"], data=data) == [
        {"a": 1, "c": 3},
        {"a": 4, "c": 6},
    ]


def test_props():
    data = {"a": 1, "b": 2, "c": 3}
    assert pamda.props(keys=["a", "c"], data=data) == [1, 3]


def test_reduce():
    assert (
        pamda.reduce(fn=pamda.add, initial_accumulator=0, data=[1, 2, 3]) == 6
    )


def test_safeDivide():
    assert pamda.safeDivide(2, 1) == 0.5
    assert pamda.safeDivide(0, 1) == 1


def test_safeDivideDefault():
    assert pamda.safeDivideDefault(5, 2, 1) == 0.5
    assert pamda.safeDivideDefault(5, 0, 1) == 0.2


def test_symmetricDifference():
    assert pamda.symmetricDifference([1, 2, 3], [2, 3, 4]) == [1, 4]


def test_tail():
    assert pamda.tail([1, 2, 3]) == 3


def test_thunkify():
    def add(a, b):
        return a + b

    thunkedAdd = pamda.thunkify(add)
    assert thunkedAdd(1, 2)() == 3


def test_unnest():
    assert pamda.unnest([["a", "b"], ["c", "d"]]) == ["a", "b", "c", "d"]
    assert pamda.unnest([["a", "b"], ["c", ["d"]]]) == ["a", "b", "c", ["d"]]


def test_zip():
    assert pamda.zip(["a", "b"], [1, 2]) == [["a", 1], ["b", 2]]


def test_zipObj():
    assert pamda.zipObj(["a", "b"], [1, 2]) == {"a": 1, "b": 2}
