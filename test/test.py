"""
Test all functions in pamda
"""

from pamda import pamda as p

# accumulate
out=p.accumulate(
    fn=p.add,
    initial_accumulator=0,
    data=[1,2,3,4]
)
if out!=[1,3,6,10]:
    print('accumulate failed')

# add
out=p.add(1, 2)
if out!=3:
    print('add failed')

# adjust
out=p.adjust(
    index=1,
    fn=p.inc,
    data=[1,5,9]
)
if out!=[1,6,9]:
    print('adjust failed')

# assocPath
data={'a':{'b':1}}
out=p.assocPath(path=['a','c'], value=3, data=data)
if out!={'a':{'b':1, 'c':3}}:
    print('assocPath failed')

data={'a':{'b':1}}
out=p.assocPath(path=['a','b','c'], value=3, data=data)
if out!={'a':{'b':{'c':3}}}:
    print('assocPath failed')

#assocPathComplex
data={'a':{'b':1}}
out=p.assocPathComplex(default=[2], default_fn=lambda x:x+[1], path=['a','c'], data=data)
if out!={'a':{'b':1,'c':[2,1]}}:
    print('assocPathComplex failed')

#dissocPath
data={'a':{'b':1, 'c':2}}
out=p.dissocPath(path=['a','c'], data=data)
if out!={'a':{'b':1}}:
    print('dissocPath failed')

#hasPath
data={'a':{'b':1}}
if not p.hasPath(path=['a','b'], data=data) or p.hasPath(path=['a','c'], data=data):
    print('hasPath failed')
