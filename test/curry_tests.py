import pytest
from pamda import pamda


def test_curry_wrapper():
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

    my_function0()
    my_function1()


def test_curry_with_defaults():
    @pamda.curry
    def my_function(a, b, c=1):
        return a + b + c

    assert my_function(1)(1) == 3


def test_thunkify_with_defaults():
    @pamda.thunkify
    def my_function(a, b, c=1):
        return a + b + c

    assert my_function(1)(1)() == 3
    assert my_function(1)(1)(2)() == 4
