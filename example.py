from pamda import pamda

data=[['a','b'],[1,2]]
pamda.flatten(data=data) #=> ['a','b',1,2]

data={'a':{'b':1}}
pamda.path(data=data, path=['a','b']) #=> 1

data={'a':{'b':1}}
pamda.hasPath(data=data, path=['a','b']) #=> True
pamda.hasPath(data=data, path=['a','d']) #=> False

data={'a':{'b':1}}
pamda.assocPath(data=data, path=['a','c'], value=3) #=> {'a':{'b':1, 'c':3}}

data={'a':{'b':1}}
pamda.assocPathComplex(data=data, path=['a','b'], default=[]) #=> {'a':{'b':1}}
pamda.assocPathComplex(data=data, path=['a','c'], default=[]) #=> {'a':{'b':1, 'c':[]}}
pamda.assocPathComplex(data=data, path=['a','d'], default=[2], default_fn=lambda x:x+[1]) #=> {'a':{'b':1,'c':[],'d':[2,1]}}

data={'a':{'b':{'c':0,'d':1}}}
pamda.dissocPath(data=data, path=['a','b','c']) #=> {'a':{'b':{'d':1}}}


data=[{'a':{'b':1, 'c':'d'}},{'a':{'b':2, 'c':'e'}}]
pamda.pluck(data=data, path=['a','b']) #=> [1,2]
pamda.pluckIf(if_path=['a','c'], if_vals=['d'], data=data, path=['a','b']) #=> [1]

data=[
    {'x_1':'a','x_2':'b', 'output':'c'},
    {'x_1':'a','x_2':'b', 'output':'d'},
    {'x_1':'a','x_2':'e', 'output':'f'}
]
pamda.nest(
    data=data,
    path_keys=['x_1','x_2'],
    value_key='output'
) #=> {'a':{'b':['c','d'], 'e':['f']}}
