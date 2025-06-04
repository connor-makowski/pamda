"""
# Pamda
[![PyPI version](https://badge.fury.io/py/pamda.svg)](https://badge.fury.io/py/pamda)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python wrapper for functional programming in object oriented structures.

Inspired heavily by [Ramda](https://ramdajs.com/docs/).


## Documentation for Pamda Functions
https://connor-makowski.github.io/pamda/pamda/pamda.html

## Key Features

- Simplified functional programming for python
- Core Functions include:
  - `curry` arbitrary methods and functions
  - `thunkify` arbitrary methods and functions
  - `pipe` data iteratively through n functions
- List based path access and features for nested dictionaries


## Setup

Make sure you have Python 3.9.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install pamda
```

## Getting Started

### Basic Usage
```py
from pamda import pamda

data={'a':{'b':1, 'c':2}}
# Example: Select data given a path and a dictionary
pamda.path(['a','b'])(data) #=> 1

# See documentation for all core pamda functions at
# https://connor-makowski.github.io/pamda/pamda.html
```

### Curry Usage
```py
from pamda import pamda

# Define a function that you want to curry
def myFunction(a,b,c):
    return [a,b,c]

# You can call pamda.curry as a function to curry your functions
curriedMyFn=pamda.curry(myFunction)

# Inputs can now be passed in an async fashion
# The function is evaluated when all inputs are added
x=curriedMyFn(1,2)
x(3) #=> [1,2,3]
x(4) #=> [1,2,4]

# Each set of inputs returns a callable function
# You can stack inputs on a single line for clean functional programming
curriedMyFn(1,2)(3) #=> [1,2,3]
```

For enforcing types, pamda relies on [type_enforced](https://github.com/connor-makowski/type_enforced) but curried objects do not play nice with `type_enforced` objects. To fix this, there is a special curry function, `curryType`, that enables type_enforced annotations for your curried functions:

```py
>>> from pamda import pamda
>>>
>>> # Pamda CurryTyped
>>> @pamda.curryTyped
... def add(a:int,b:int):
...     return a+b
...
>>> add(1)(1)
2
>>> add(1)(1.5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/conmak/development/personal/pamda/pamda/pamda_curry.py", line 43, in __call__
    results = self.__fnExecute__(*new_args, **new_kwargs)
  File "/home/conmak/development/personal/pamda/venv/lib/python3.10/site-packages/type_enforced/enforcer.py", line 90, in __call__
    self.__check_type__(assigned_vars.get(key), value, key)
  File "/home/conmak/development/personal/pamda/venv/lib/python3.10/site-packages/type_enforced/enforcer.py", line 112, in __check_type__
    self.__exception__(
  File "/home/conmak/development/personal/pamda/venv/lib/python3.10/site-packages/type_enforced/enforcer.py", line 34, in __exception__
    raise TypeError(f"({self.__fn__.__qualname__}): {message}")
TypeError: (add): Type mismatch for typed variable `b`. Expected one of the following `[<class 'int'>]` but got `<class 'float'>` instead.
```


### Thunkify Usage
```py
from pamda import pamda

# Define a function that you want to thunkify
# thunkify can be called as a function or decorator
@pamda.thunkify
def myFunction(a,b,c):
    return [a,b,c]

# The function is now curried and the evaluation is lazy
# This means the function is not evaluated until called
x=myFunction(1,2)
x(3) #=> <pamda.curry_obj object at 0x7fd514e4c820>
x(3)() #=> [1,2,3]

y=x(4)
y() #=> [1,2,4]
```

Thunkified functions can be executed asynchronously.

```py
from pamda import pamda
import time

@pamda.thunkify
def test(name, wait):
    print(f'{name} start')
    time.sleep(wait)
    print(f'{name} end')
    return wait

async_test_a = pamda.asyncRun(test('a',2))
async_test_b = pamda.asyncRun(test('b',1))
async_test_a.asyncWait()
async_test_c = pamda.asyncRun(test('c',1))
```

The above code would output:
```
a start
b start
b end
a end
c start
c end
```

### Pipe
```py
from pamda import pamda

def square(x):
    return x**2

def half(x):
    return x/2

def negate(x):
    return -x

# You can pipe data through multiple functions for clean functional programming
pamda.pipe([square, half, negate])(args=(6,),kwargs={}) #=> -18
```

### Use pamda as a subclass
```py
from pamda import pamda

class myClass(pamda):
    def myFunction(self, a):
        return self.inc(a)

mc=myClass()
mc.myFunction(2) #=> 3

@mc.curry
def addUp(a,b):
    return a+b

addUp(1)(2) #=> 3
```

## Pamda Utils

- Pamda also ships with a few helpful utilities
- Check out the documentation here:
  - https://connor-makowski.github.io/pamda/pamda_utils.html"""
from .pamda import pamda
