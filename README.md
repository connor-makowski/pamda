Pamda
==========
Python wrapper for object oriented processes similar to [Ramda](https://ramdajs.com/docs/).


Full Documentation
--------
https://connor-makowski.github.io/pamda/

Features
--------

- Simplified python access for certain Ramda functions.

Setup
----------

Make sure you have Python 3.6.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install pamda
```

### Example
```py
from pamda import pamda as p

data=[['a','b'],[1,2]]
p.flatten(data=data) #=> ['a','b',1,2]
```
