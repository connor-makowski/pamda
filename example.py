from pamda import pamda as p

data=[['a','b'],[1,2]]
p.flatten(data=data) #=> ['a','b',1,2]

data={'a':{'b':1}}
p.path(data=data, path=['a','b']) #=> 1

data={'a':{'b':1}}
p.hasPath(data=data, path=['a','b']) #=> True
p.hasPath(data=data, path=['a','d']) #=> False

data={'a':{'b':1}}
p.assocPath(data=data, path=['a','c'], value=3) #=> {'a':{'b':1, 'c':3}}

data={'a':{'b':1}}
p.assocPathComplex(data=data, path=['a','b'], default=[]) #=> {'a':{'b':1}}
p.assocPathComplex(data=data, path=['a','c'], default=[]) #=> {'a':{'b':1, 'c':[]}}
p.assocPathComplex(data=data, path=['a','d'], default=[2], default_func=lambda x:x+[1]) #=> {'a':{'b':1,'c':[],'d':[2,1]}}

data={'a':{'b':{'c':0,'d':1}}}
p.dissocPath(data=data, path=['a','b','c']) #=> {'a':{'b':{'d':1}}}


data=[{'a':{'b':1, 'c':'d'}},{'a':{'b':2, 'c':'e'}}]
p.pluck(data=data, path=['a','b']) #=> [1,2]
p.pluck(data=data, path=['a','b'], if_path=['a','c'], if_vals=['d']) #=> [1]

data=[
    {'x_1':'a','x_2':'b', 'output':'c'},
    {'x_1':'a','x_2':'b', 'output':'d'},
    {'x_1':'a','x_2':'e', 'output':'f'}
]
p.nest(
    data=data,
    nest_by_variables=['x_1','x_2'],
    nest_output_variable='output'
) #=> {'a':{'b':['c','d'], 'e':['f']}}
