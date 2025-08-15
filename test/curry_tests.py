"""
Test all functions in pamda
"""

print("\n===============\n Curry Tests:\n===============")

from pamda import pamda


@pamda.curry
def my_fn_wrapper(fn, delay=0):
    def wrapped(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapped


@my_fn_wrapper()
def my_function0():
    return "Hello, World!"


@my_fn_wrapper(delay=1)
def my_function1():
    return "Hello, Universe!"


try:
    my_function0()
    my_function1()
except Exception as e:
    print(f"Curry Wrapper Test Failed: {e}")


@pamda.curry
def my_function2(a, b, c=1):
    return a + b + c


if my_function2(1)(1) != 3:
    print("Curry Function Test Failed")


@pamda.thunkify
def my_function3(a, b, c=1):
    return a + b + c


if my_function3(1)(1)() != 3 or my_function3(1)(1)(2)() != 4:
    print("Curry Function Test Failed")
