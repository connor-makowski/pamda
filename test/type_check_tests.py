"""
Test type_checking in pamda
"""

print("\n===============\nType Checking Tests:\n===============")
from pamda import pamda

all_pass = True


@pamda.curryTyped
def my_fn(a: int, b: list[str]) -> str:
    return str(a) + b[0]


try:
    x = my_fn(1)
except:
    x = None

try:
    x(["2"])
except:
    all_pass = False

try:
    x([2])
    all_pass = False
except:
    pass

try:
    x(2)
    all_pass = False
except:
    pass

if not all_pass:
    print("Type check test failed")

print("Type Checking Tests: PASS" if all_pass else "Type Checking Tests: FAIL")
