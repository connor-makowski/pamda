"""
Test type_checking in pamda
"""

print("\n===============\nType Checking Tests:\n===============")
from pamda import pamda


@pamda.curryTyped
def my_fn(a: int, b: list[str]) -> str:
    return str(a) + b[0]


try:
    x = my_fn(1)
except:
    x = None

isPassing = True

try:
    x(["2"])
except:
    isPassing = False

try:
    x([2])
    isPassing = False
except:
    pass

try:
    x(2)
    isPassing = False
except:
    pass

if not isPassing:
    print("Type check test failed")
