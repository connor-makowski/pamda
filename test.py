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

#assocPathComplex
data={'a':{'b':1}}
out=p.assocPathComplex(default=[2], default_fn=lambda x:x+[1], path=['a','c'], data=data)
if out!={'a':{'b':1,'c':[2,1]}}:
    print('assocPathComplex failed')
