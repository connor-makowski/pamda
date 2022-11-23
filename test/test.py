"""
Test all functions in pamda
"""

from pamda import pamda

# accumulate
out=pamda.accumulate(
    fn=pamda.add,
    initial_accumulator=0,
    data=[1,2,3,4]
)
if out!=[1,3,6,10]:
    print('accumulate failed')

# add
out=pamda.add(1, 2)
if out!=3:
    print('add failed')

# adjust
out=pamda.adjust(
    index=1,
    fn=pamda.inc,
    data=[1,5,9]
)
if out!=[1,6,9]:
    print('adjust failed')

# assocPath
data={'a':{'b':1}}
out=pamda.assocPath(path=['a','c'], value=3, data=data)
if out!={'a':{'b':1, 'c':3}}:
    print('assocPath failed')

data={'a':{'b':1}}
out=pamda.assocPath(path=['a','b','c'], value=3, data=data)
if out!={'a':{'b':{'c':3}}}:
    print('assocPath failed')

data={'a':['b','c','d']}
out=pamda.assocPath(path=['a',1], value='e', data=data)
if out!={'a':['b','e','d']}:
    print('assocPath failed')

#assocPathComplex
data={'a':{'b':1}}
out=pamda.assocPathComplex(default=[2], default_fn=lambda x:x+[1], path=['a','c'], data=data)
if out!={'a':{'b':1,'c':[2,1]}}:
    print('assocPathComplex failed')

#dissocPath
data={'a':{'b':1, 'c':2}}
out=pamda.dissocPath(path=['a','c'], data=data)
if out!={'a':{'b':1}}:
    print('dissocPath failed')

#hasPath
data={'a':{'b':1}}
if not pamda.hasPath(path=['a','b'], data=data) or pamda.hasPath(path=['a','c'], data=data):
    print('hasPath failed')
