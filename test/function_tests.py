"""
Test all functions in pamda
"""

print("\n===============\nFunction Tests:\n===============")
from pamda import pamda

# accumulate
out = pamda.accumulate(fn=pamda.add, initial_accumulator=0, data=[1, 2, 3, 4])
if out != [1, 3, 6, 10]:
    print("accumulate failed")

# add
out = pamda.add(1, 2)
if out != 3:
    print("add failed")

# adjust
out = pamda.adjust(index=1, fn=pamda.inc, data=[1, 5, 9])
if out != [1, 6, 9]:
    print("adjust failed")

# assocPath
data = {"a": {"b": 1}}
out = pamda.assocPath(path=["a", "c"], value=3, data=data)
if out != {"a": {"b": 1, "c": 3}}:
    print("assocPath failed")

data = {("a", "b"): 1}
out = pamda.assocPath(path=("a", "c"), value=3, data=data)
if out != {("a", "b"): 1, ("a", "c"): 3}:
    print("assocPath failed")

data = {"a": {"b": 1}}
out = pamda.assocPath(path=["a", "b", "c"], value=3, data=data)
if out != {"a": {"b": {"c": 3}}}:
    print("assocPath failed")

data = {"a": ["b", "c", "d"]}
out = pamda.assocPath(path=["a", 1], value="e", data=data)
if out != {"a": ["b", "e", "d"]}:
    print("assocPath failed")

data = {"a": [{"b": 1}, {"b": 2}]}
out = pamda.assocPath(path=["a", 1, "b"], value=3, data=data)
if out != {"a": [{"b": 1}, {"b": 3}]}:
    print("assocPath failed")


# assocPathComplex
data = {"a": {"b": 1}}
out = pamda.assocPathComplex(
    default=[2], default_fn=lambda x: x + [1], path=["a", "c"], data=data
)
if out != {"a": {"b": 1, "c": [2, 1]}}:
    print("assocPathComplex failed")

# asyncRun
# See general_tests.py

# asyncWait
# See general_tests.py

# clamp
if pamda.clamp(1, 10, 11) != 10 or pamda.clamp(1, 10, 0) != 1:
    print("clamp failed")


# curry
def add(a, b):
    return a + b


curried_add = pamda.curry(add)
if curried_add(1)(2) != 3:
    print("curry failed")


# curryTyped
def add(a: int, b: int) -> int:
    return a + b


curry_typed_add = pamda.curryTyped(add)
try:
    curry_typed_add(1)(2)
except:
    print("curryTyped failed")

try:
    curry_typed_add(1.5)(2.5)
    print("curryTyped failed")
except:
    pass

# dec
if pamda.dec(1) != 0:
    print("dec failed")

# dissocPath
data = {"a": {"b": 1, "c": 2}}
out = pamda.dissocPath(path=["a", "c"], data=data)
if out != {"a": {"b": 1}}:
    print("dissocPath failed")

# hasPath
data = {"a": {"b": 1}}
if not pamda.hasPath(path=["a", "b"], data=data) or pamda.hasPath(
    path=["a", "c"], data=data
):
    print("hasPath failed")

# difference
if pamda.difference([1, 2, 3], [2, 3, 4]) != [1]:
    print("difference failed")

# dissocPath
data = {"a": {"b": 1, "c": 2}}
out = pamda.dissocPath(path=["a", "c"], data=data)
if out != {"a": {"b": 1}}:
    print("dissocPath failed")

# flatten
if pamda.flatten([1, 2, [3, [4]]]) != [1, 2, 3, 4]:
    print("flatten failed (0)")

if pamda.flatten(data=[["a", "b"], [1, 2]]) != ["a", "b", 1, 2]:
    print("flatten failed (1)")


# flip
def doubleA(a, b):
    return a * 2


if pamda.flip(doubleA)(1, 2) != 4:
    print("flip failed")


# getArity
def add(a, b):
    return a + b


if pamda.getArity(add) != 2:
    print("getArity failed")


# groupBy
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
    "C": [{"name": "Connor", "score": 75}, {"name": "Fred", "score": 79}],
}

if pamda.groupBy(getGrade, data) != expected:
    print("groupBy failed")

# groupKeys
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
if pamda.groupKeys(["color", "shape"], data) != expected:
    print("groupKeys failed")


# groupWith
def areEqual(a, b):
    return a == b


data = [1, 2, 3, 1, 1, 2, 2, 3, 3, 3]
expected = [[1], [2], [3], [1, 1], [2, 2], [3, 3, 3]]
if pamda.groupWith(areEqual, data) != expected:
    print("groupWith failed")

# hasPath
data = {"a": {"b": 1}}
if not pamda.hasPath(path=["a", "b"], data=data) or pamda.hasPath(
    path=["a", "c"], data=data
):
    print("hasPath failed")

# hardRound
if pamda.hardRound(2, 1.2345) != 1.23 or pamda.hardRound(0, 1.2345) != 1:
    print("hardRound failed")

# head
if pamda.head([1, 2, 3]) != 1:
    print("head failed")

if pamda.head("abc") != "a":
    print("head failed")

# inc
if pamda.inc(1) != 2:
    print("inc failed")

# intersection
if pamda.intersection([1, 2, 3], [2, 3, 4]) != [2, 3]:
    print("intersection failed")

# map
if pamda.map(pamda.inc, [1, 2, 3]) != [2, 3, 4]:
    print("map failed")

# mean
if pamda.mean([1, 2, 3]) != 2:
    print("mean failed")

# median
if pamda.median([1, 2, 3]) != 2:
    print("median failed")

# mergeDeep
data1 = {"a": {"b": 1, "c": 2}}
data2 = {"a": {"b": 3, "d": 4}}
expected = {"a": {"b": 3, "c": 2, "d": 4}}
if pamda.mergeDeep(update_data=data2, data=data1) != expected:
    print("mergeDeep failed")

# nest
data = [
    {"x_1": "a", "x_2": "b", "output": "c"},
    {"x_1": "a", "x_2": "b", "output": "d"},
    {"x_1": "a", "x_2": "e", "output": "f"},
]
expected = {"a": {"b": ["c", "d"], "e": ["f"]}}
out = pamda.nest(path_keys=["x_1", "x_2"], value_key="output", data=data)
if out != expected:
    print("nest failed")

# nestItem
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
out = pamda.nestItem(path_keys=["x_1", "x_2"], data=data)
if out != expected:
    print("nestItem failed")

# path
data = {"a": {"b": 1}, "c": [2]}
if pamda.path(path=["a", "b"], data=data) != 1 or pamda.path(path=["c", 0], data=data) != 2:
    print("path failed")

# pathOr
data = {"a": {"b": 1}, "c": [2]}
if (
    pamda.pathOr(default=2, path=["a", "b"], data=data) != 1
    or pamda.pathOr(default=2, path=["a", "c"], data=data) != 2
    or pamda.pathOr(default=3, path=["c", 0], data=data) != 2
    or pamda.pathOr(default=3, path=["c", 1], data=data) != 3
):
    print("pathOr failed")


# pipe
def add(a, b):
    return a + b


def double(a):
    return a * 2


if pamda.pipe(fns=[add, double], args=(1, 2), kwargs={}) != 6:
    print("pipe failed (0)")

data = ["abc", "def"]
if pamda.pipe(fns=[pamda.head, pamda.tail], args=(data,), kwargs={}) != "c":
    print("pipe failed (1)")
if (
    pamda.pipe(fns=[pamda.head, pamda.tail], args=(), kwargs={"data": data})
    != "c"
):
    print("pipe failed (2)")

data = {"a": {"b": "c"}}
curriedPath = pamda.curry(pamda.path)
if pamda.pipe(fns=[curriedPath(["a", "b"])], args=(data,), kwargs={}) != "c":
    print("pipe failed (3)")

# pivot
data = [
    {"a": "a1", "b": "b1", "c": "c1"},
    {"a": "a2", "b": "b2", "c": "c2"},
]
expected = {"a": ["a1", "a2"], "b": ["b1", "b2"], "c": ["c1", "c2"]}
if pamda.pivot(data) != expected:
    print("pivot failed (0)")

data = {"a": ["a1", "a2"], "b": ["b1", "b2"], "c": ["c1", "c2"]}
expected = [
    {"a": "a1", "b": "b1", "c": "c1"},
    {"a": "a2", "b": "b2", "c": "c2"},
]
if pamda.pivot(data) != expected:
    print("pivot failed (1)")

# pluck
data = [{"a": {"b": 1, "c": "d"}}, {"a": {"b": 2, "c": "e"}}]
if pamda.pluck(path=["a", "b"], data=data) != [1, 2]:
    print("pluck failed")

# pluckIf
data = [{"a": {"b": 1, "c": "d"}}, {"a": {"b": 2, "c": "e"}}]
if pamda.pluckIf(fn=lambda x: x["a"]["b"] == 1, path=["a", "c"], data=data) != [
    "d"
]:
    print("pluckIf failed")

# project
data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
if pamda.project(keys=["a", "c"], data=data) != [
    {"a": 1, "c": 3},
    {"a": 4, "c": 6},
]:
    print("project failed")

# props
data = {"a": 1, "b": 2, "c": 3}
if pamda.props(keys=["a", "c"], data=data) != [1, 3]:
    print("props failed")

# reduce
if pamda.reduce(fn=pamda.add, initial_accumulator=0, data=[1, 2, 3]) != 6:
    print("reduce failed")

# safeDivide
if pamda.safeDivide(2, 1) != 0.5 or pamda.safeDivide(0, 1) != 1:
    print("safeDivide failed")

# safeDivideDefault
if (
    pamda.safeDivideDefault(5, 2, 1) != 0.5
    or pamda.safeDivideDefault(5, 0, 1) != 0.2
):
    print("safeDivideDefault failed")

# symmetricDifference
if pamda.symmetricDifference([1, 2, 3], [2, 3, 4]) != [1, 4]:
    print("symmetricDifference failed")

# tail
if pamda.tail([1, 2, 3]) != 3:
    print("tail failed")


# thunkify
def add(a, b):
    return a + b


thunkedAdd = pamda.thunkify(add)
if thunkedAdd(1, 2)() != 3:
    print("thunkify failed")

# unnest
data = [["a", "b"], ["c", "d"]]
if pamda.unnest(data) != ["a", "b", "c", "d"]:
    print("unnest failed (0)")

data = [["a", "b"], ["c", ["d"]]]
if pamda.unnest(data) != ["a", "b", "c", ["d"]]:
    print("unnest failed (1)")

# zip
if pamda.zip(["a", "b"], [1, 2]) != [["a", 1], ["b", 2]]:
    print("zip failed")

# zipObj
if pamda.zipObj(["a", "b"], [1, 2]) != {"a": 1, "b": 2}:
    print("zipObj failed")
