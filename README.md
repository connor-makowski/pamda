Pamda
==========
Python wrapper for functional programming in object oriented structures

Inspired heavily by [Ramda](https://ramdajs.com/docs/).


Documentation for Pamda
--------
https://connor-makowski.github.io/pamda/pamda_class.html

Key Features
--------

- Simplified functional programming for python
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
# Access a data path from a dictionary
p.path(path=['a','b'], data=data) #=> 1
# See all pamda functions at
# https://connor-makowski.github.io/pamda/pamda_class.html
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

# Each set of inputs returns a function
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
x(3) #=> <pamda.pamda_utils.curry_class object at 0x7fd514e4c820>
x(3)() #=> [1,2,3]

y=x(4)
y() #=> [1,2,4]
```

## Pre-curried Pamda Usage
```py
# Pamda functions are not curried by default
# Instead of
# from pamda import pamda as p
# You can use:
from pamda import pamda_curried as p
# This curries all pamda functions for you automatically
# Note: help functions currently break when importing from pamda_curried
data={'a':{'b':1, 'c':2}}
p.path(['a','b'])(data) #=> 1
```

## Pipe
```py
from pamda import pamda_curried as p

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

# Pamdata getting Started

- Pamda also ships with a few helpful data utilities
- Check out the documentation here:
  - https://connor-makowski.github.io/pamda/pamdata_class.html

```py
from pamda import pamdata as pdata

pdata.read_csv(filename='myfile.csv')
```
