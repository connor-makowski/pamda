Pamda
==========
Python wrapper for object oriented processes similar to [Ramda](https://ramdajs.com/docs/).


Documentation for Pamda
--------
https://connor-makowski.github.io/pamda/pamda_class.html

Documentation for Pamdata (simplified data access)
--------
https://connor-makowski.github.io/pamda/pamdata_class.html

Features
--------

- Simplified python access for certain Ramda and python data functions.

Setup
----------

Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install pamda
```

### Choice Examples Highlight key Pamda features
```py
from pamda import pamda as p

# Path
data={'a':{'b':1, 'c':2}}
p.path(path=['a','b'], data=data) #=> 1

# Curry
def myFunction(a,b,c):
    return [a,b,c]

curriedMyFn=p.curry(myFunction)
x=curriedMyFn(1,2)
x(3) #=> [1,2,3]
x(4) #=> [1,2,4]

data={'a':{'b':1, 'c':2}}
curriedPath=p.curry(p.path)
abPath=curriedPath(['a','b'])
abPath(data=data) #=> 1

# Pipe
def square(x):
  return x**2

def half(x):
  return x/2

def negate(x):
  return -x

p.pipe(fns=[square, half, negate], data=6) #=> -18
```

```py
from pamda import pamdata as pdata

pdata.read_csv(filename='myfile.csv')
```
