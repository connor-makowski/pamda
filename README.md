Pamda
==========
Python wrapper for functional programming in object oriented structures

Inspired heavily by [Ramda](https://ramdajs.com/docs/).


Documentation for Pamda Functions
--------
https://connor-makowski.github.io/pamda/pamda_core.html

Key Features
--------

- Simplified functional programming for python
- Core Functions include:
  - `curry` arbitrary methods and functions
  - `thunkify` arbitrary methods and functions
  - `pipe` data iteratively through n functions
- List based path access and features for nested dictionaries


Setup
----------

Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install pamda
```

# Getting Started

## Basic Usage
```py
from pamda import pamda as p

data={'a':{'b':1, 'c':2}}
# Example: Select data given a path and a dictionary
p.path(['a','b'])(data) #=> 1

# See documentation for all core pamda functions at
# https://connor-makowski.github.io/pamda/pamda_core.html
```

## Curry Usage
```py
from pamda import pamda as p

# Define a function that you want to curry
def myFunction(a,b,c):
    return [a,b,c]

# You can call p.curry as a function to curry your functions
curriedMyFn=p.curry(myFunction)

# Inputs can now be passed in an async fashion
# The function is evaluated when all inputs are added
x=curriedMyFn(1,2)
x(3) #=> [1,2,3]
x(4) #=> [1,2,4]

# Each set of inputs returns a callable function
# You can stack inputs on a single line for clean functional programming
curriedMyFn(1,2)(3) #=> [1,2,3]
```

```py
from pamda import pamda as p

# You can use p.curry as a decorator too
@p.curry
def myFunction(a,b,c):
    return [a,b,c]

myFunction(1,2)(4) #=> [1,2,4]
```

## Thunkify Usage
```py
from pamda import pamda as p

# Define a function that you want to thunkify
# thunkify can be called as a function or decorator
@p.thunkify
def myFunction(a,b,c):
    return [a,b,c]

# The function is now curried and the evaluation is lazy
# This means the function is not evaluated until called
x=myFunction(1,2)
x(3) #=> <pamda.curry_fn object at 0x7fd514e4c820>
x(3)() #=> [1,2,3]

y=x(4)
y() #=> [1,2,4]
```

## Pipe
```py
from pamda import pamda as p

def square(x):
  return x**2

def half(x):
  return x/2

def negate(x):
  return -x

data=6
# You can pipe data through multiple functions for clean functional programming
p.pipe([square, half, negate])(data) #=> -18
```

# Pamda Core Usage

Importing `pamda` or `pamda_uncurried` creates an initialized `pamda_core` instance. If you want access to the uninitialized `pamda` class methods, you can access them via `pamda_core`

`pamda_core`:
  - Contains all `pamda` methods
  - All methods are not curried by default
  - Can be used for a subclass for inheritence purposes

## Create your own uncurried pamda instance
```py
from pamda import pamda_core
p=pamda_core()
data={'a':{'b':1, 'c':2}}
# Remember that pamda_core methods are not curried by default
p.path(['a','b'], data) #=> 1
```

## Use pamda_core as a subclass
```py
from pamda import pamda_core

class myClass(pamda_core):
  def myFunction(self, a):
    return self.inc(a)

mc=myClass()
mc.myFunction(2) #=> 3

@mc.curry
def addUp(a,b):
  return a+b

addUp(1)(2) #=> 3
```

# Pamda Utils

- Pamda also ships with a few helpful utilities
- Check out the documentation here:
  - https://connor-makowski.github.io/pamda/utils.html
