from pamda.utils import utils
from pamda.curry_fn import curry_fn

class pamda_core(utils):
    def add(self, a, b):
        """
        Function:

        - Adds two numbers

        Requires:

        - `a`:
            - Type: int | float
            - What: The first number to add
        - `b`:
            - Type: int | float
            - What: The second number to add

        Example:

        ```
        p.add(1, 2) #=> 3
        ```
        """
        if not all([isinstance(item, (int,float)) for item in [a, b]]):
            self.exception('`a` and `b` both have to be `int`s or `float`s')
        return a+b

    def adjust(self, index, fn, data):
        """
        Function:

        - Adjusts an item in a list by applying a function to it

        Requires:

        - `index`:
            - Type: int
            - What: The 0 based index of the item in the list to adjust
            - Note: Indicies are accepted
            - Note: If the index is out of range, picks the (-)first / (+)last item
        - `fn`:
            - Type: function | method
            - What: The function to apply the index item to
            - Note: This is automatically curried
        - `data`:
            - Type: list
            - What: The list to adjust

        Example:

        ```
        data=[1,5,9]
        p.adjust(
            index=1,
            fn=p.inc,
            data=data
        ) #=> [1,6,9]
        ```
        """
        if not isinstance(index, int):
            self.exception('`index` must be an int')
        if not isinstance(data, list):
            self.exception('`data` must be a list')
        if not isinstance(fn, curry_fn):
            fn=curry_fn(fn)
        index=self.clamp(-len(data),len(data)-1,index)
        data[index]=fn(data[index])
        return data

    def assocPath(self, path, value, data):
        """
        Function:

        - Ensures a path exists within a nested dictionary

        Requires:

        - `path`:
            - Type: list of strs | str
            - What: The path to check
            - Note: If a string is passed, assumes a single item path list with that string
        - `value`:
            - Type: any
            - What: The value to appropriate to the end of the path
        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists

        Example:

        ```
        data={'a':{'b':1}}
        p.assocPath(path=['a','c'], value=3, data=data) #=> {'a':{'b':1, 'c':3}}
        ```
        """
        if isinstance(path, str):
            path=[path]
        if len(path) > 1:
            if path[0] not in data:
                data[path[0]] = {}
            data[path[0]] = self.assocPath(data=data[path[0]], path=path[1:],value=value)
            return data
        else:
            data[path[0]] = value
            return data

    def assocPathComplex(self, default, default_fn, path, data):
        """
        Function:

        - Ensures a path exists within a nested dictionary

        Requires:

        - `default`:
            - Type: any
            - What: The default item to add to a path that does not yet exist
        - `default_fn`:
            - Type: function | method
            - What: A unary (single input) function that takes in the current path item (or default) and adjusts it
            - Example: `lambda x: x` # Returns the value in the dict or the default value if none was present
        - `path`:
            - Type: list of strs
            - What: The path to check
        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists

        Example:

        ```
        data={'a':{'b':1}}
        p.assocPathComplex(default=[2], default_fn=lambda x:x+[1], path=['a','c'], data=data) #=> {'a':{'b':1,'c':[2,1]}}
        ```
        """
        if len(path) > 1:
            if path[0] not in data:
                data[path[0]] = {}
            data[path[0]] = self.assocPathComplex(data=data[path[0]], path=path[1:], default=default, default_fn=default_fn)
            return data
        else:
            if self.getArity(default_fn)!=1:
                self.exception('`assocPathComplex` `default_fn` must be an unary (single input) function.')
            if path[0] not in data:
                data[path[0]] = default
            data[path[0]] = default_fn(data[path[0]])
            return data

    def clamp(self, minimum, maximum, a):
        """
        Function:

        - Forces data to be within minimum and maximum

        Requires:

        - `minimum`:
            - Type: int | float
            - What: The minimum number
        - `maximum`:
            - Type: int | float
            - What: The maximum number
        - `a`:
            - Type: int | float
            - What: The number to clamp

        Example:

        ```
        p.clamp(1, 3, 2) #=> 2
        p.clamp(1, 3, 5) #=> 3
        ```
        """
        if not all([isinstance(item, (int,float)) for item in [minimum, maximum, a]]):
            self.exception('`minimum`,`maximum` and `a` all have to be `int`s or `float`s')
        return min(max(a,minimum),maximum)

    def curry(self, fn):
        """
        Function:

        - Curries a function such that inputs can be added interatively

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to curry
            - Note: Class methods auto apply self during curry

        Notes:

        - Once curried, the function | method becomes a curry_fn object
        - The initial function is only called once all inputs are passed


        Examples:

        ```
        curriedZip=p.curry(p.zip)
        curriedZip(['a','b'])([1,2]) #=> [['a',1],['b',2]]

        # Curried functions can be thunkified at any time
        # See also thunkify
        zipThunk=curriedZip.thunkify()(['a','b'])([1,2])
        zipThunk() #=> [['a',1],['b',2]]
        ```

        ```
        def myFunction(a,b,c):
            return [a,b,c]

        curriedMyFn=p.curry(myFunction)

        curriedMyFn(1,2,3) #=> [1,2,3]
        curriedMyFn(1)(2,3) #=> [1,2,3]

        x=curriedMyFn(1)(2)
        x(3) #=> [1,2,3]
        x(4) #=> [1,2,4]


        ```
        """
        if not isinstance(fn, curry_fn):
            return curry_fn(fn)
        return fn

    def dec(self, a):
        """
        Function:

        - Decrements a number by one

        Requires:

        - `a`:
            - Type: int | float
            - What: The number to decrement

        Example:

        ```
        p.dec(42) #=> 41
        ```
        """
        if not isinstance(a, (int, float)):
            self.exception('`a` must be an `int` or a `float`')
        return a-1

    def difference(self, a, b):
        """
        Function:

        - Combines two lists into a list of no duplicates items present in the first list but not the second

        Requires:

        - `a`:
            - Type: list
            - What: List of items in which to look for a difference
        - `b`:
            - Type: list
            - What: List of items in which to compare when looking for the difference

        Example:

        ```
        a=['a','b']
        b=['b','c']
        p.difference(a=a, b=b) #=> ['a']
        p.difference(a=b, b=a) #=> ['c']
        ```
        """
        return list(set(a).difference(set(b)))

    def dissocPath(self, path, data):
        """
        Function:

        - Removes the value at the end of a path within a nested dictionary

        Requires:

        - `path`:
            - Type: list of strs | str
            - What: The path to remove from the dictionary
            - Note: If a string is passed, assumes a single item path list with that string
        - `data`:
            - Type: dict
            - What: A dictionary with a path to be removed

        Example:

        ```
        data={'a':{'b':{'c':0,'d':1}}}
        p.dissocPath(path=['a','b','c'], data=data) #=> {'a':{'b':{'d':1}}}
        ```
        """
        if isinstance(path, str):
            path=[path]
        if not self.hasPath(data, path):
            self.warn(message="Path does not exist")
            return data
        if len(path)==0:
            return {}
        return self.assocPath(data=data, path=path[:-1], value={key:value for key, value in self.path(data, path=path[:-1]).items() if key!=path[-1]})

    def flatten(self, data):
        """
        Function:

        - Flattens a list of lists to a single list

        Requires:

        - `data`:
            - Type: list of lists
            - What: The list of lists to reduce to a single list
        Example:

        ```
        data=[['a','b'],[1,2]]
        p.flatten(data=data) #=> ['a','b',1,2]
        ```
        """
        return [i for sub_list in data for i in sub_list]

    def getArity(self, fn):
        """
        Function:

        - Gets the arity (number of inputs left to be specified) of a function or method (curried or uncurried)

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to get the arity of
            - Note: Class methods remove one arity to account for self

        Examples:

        ```
        p.getArity(p.zip) #=> 2
        curriedZip=p.curry(p.zip)
        ABCuriedZip=curriedZip(['a','b'])
        p.getArity(ABCuriedZip) #=> 1
        ```
        """
        if isinstance(fn, curry_fn):
            return fn.arity
        return curry_fn(fn).arity

    def hasPath(self, path, data):
        """
        Function:

        - Checks if a path exists within a nested dictionary

        Requires:

        - `path`:
            - Type: list of strs | str
            - What: The path to check
            - Note: If a string is passed, assumes a single item path list with that string
        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists

        Example:

        ```
        data={'a':{'b':1}}
        p.hasPath(path=['a','b'], data=data) #=> True
        p.hasPath(path=['a','d'], data=data) #=> False
        ```
        """
        if isinstance(path, str):
            path=[path]
        if len(path) > 0:
            if path[0] in data:
                return self.hasPath(data=data[path[0]], path=path[1:])
            else:
                return False
        return True

    def hardRound(self, decimal_places, a):
        """
        Function:

        - Rounds to a set number of decimal places regardless of floating point math in python

        Requires:

        - `a`:
            - Type: int | float
            - What: The number to round

        Optional:

        - `decimal_places`:
            - Type: int
            - What: The number of decimal places to round to
            - Default: 0
            - Notes: Negative numbers accepted (EG -1 rounds to the nearest 10)

        Example:

        ```
        a=12.345
        p.hardRound(1,a) #=> 12.3
        p.hardRound(-1,a) #=> 10
        ```
        """
        if not isinstance(a, (float, int)):
            self.exception('`hardRound` can only be called on `float` or `int` objects')
        return int(a*(10**decimal_places)+0.5)/(10**decimal_places)

    def head(self, data):
        """
        Function:

        - Picks the first item out of a list or string

        Requires:

        - `data`:
            - Type: list | str
            - What: A list or string

        Example:

        ```
        data=['fe','fi','fo','fum']
        p.first(
            data=data
        ) #=> fe
        ```
        """
        if not isinstance(data, (list,str)):
            self.exception("`head` can only be called on a `str` or a `list`")
        if not len(data)>0:
            self.exception("Attempting to call `head` on an empty list or str")
        return data[0]

    def inc(self, a):
        """
        Function:

        - Increments a number by one

        Requires:

        - `a`:
            - Type: int | float
            - What: The number to increment

        Example:

        ```
        p.inc(42) #=> 43
        ```
        """
        if not isinstance(a, (int, float)):
            self.exception('`a` must be an `int` or a `float`')
        return a+1

    def intersection(self, a, b):
        """
        Function:

        - Combines two lists into a list of no duplicates composed of those elements common to both lists

        Requires:

        - `a`:
            - Type: list
            - What: List of items in which to look for an intersection
        - `b`:
            - Type: list
            - What: List of items in which to look for an intersection

        Example:

        ```
        a=['a','b']
        b=['b','c']
        p.intersection(a=a, b=b) #=> ['b']
        ```
        """
        return list(set(a).intersection(set(b)))

    def mergeDeep(self, update_data, data):
        """
        Function:

        - Recursively merges two nested dictionaries keeping all keys at each layer
        - Values from `update_data` are used when keys are present in both dictionaries

        Requires:

        - `update_data`:
            - Type: dict
            - What: The new data that will take precedence during merging
        - `data`:
            - Type: dict
            - What: The original data that will be merged into

        Example:

        ```
        data={'a':{'b':{'c':'d'},'e':'f'}}
        update_data={'a':{'b':{'h':'i'},'e','g'}}
        p.mergeDeep(
            update_data=update_data,
            data=data
        ) #=> {'a':{'b':{'c':'d','h':'i'},'e':'g'}}
        ```
        """
        if not isinstance(data, dict) or not isinstance(update_data, dict):
            return update_data
        output=dict(data)
        keys_original=set(data.keys())
        keys_update=set(update_data.keys())
        similar_keys=keys_original.intersection(keys_update)
        similar_dict={key:self.mergeDeep(data[key], update_data[key]) for key in similar_keys}
        new_keys=keys_update.difference(keys_original)
        new_dict={key:update_data[key] for key in new_keys}
        output.update(similar_dict)
        output.update(new_dict)
        return output

    def nest(self, path_keys, value_key, data):
        """
        Function:

        - Nests a list of dictionaries into a nested dictionary
        - Similar items are appended to a list in the end of the nested dictionary

        Requires:

        - `path_keys`:
            - Type: list of strs
            - What: The variables to pull from each item in data
            - Note: Used to build out the nested dicitonary
            - Note: Order matters as the nesting occurs in order of variable
        - `value_key`:
            - Type: str
            - What: The variable to add to the list at the end of the nested dictionary path
        - `data`:
            - Type: list of dicts
            - What: A list of dictionaries to use for nesting purposes

        Example:

        ```
        data=[
            {'x_1':'a','x_2':'b', 'output':'c'},
            {'x_1':'a','x_2':'b', 'output':'d'},
            {'x_1':'a','x_2':'e', 'output':'f'}
        ]
        p.nest(
            path_keys=['x_1','x_2'],
            value_key='output',
            data=data
        ) #=> {'a':{'b':['c','d'], 'e':['f']}}
        ```
        """
        if not isinstance(data, list):
            self.exception("Attempting to `nest` an object that is not a list")
        if len(data) == 0:
            self.exception("Attempting to `nest` from an empty list")
        nested_output = {}
        for item in data:
            nested_output = self.assocPathComplex(
                data=nested_output,
                path=[item[key] for key in path_keys],
                default=[],
                default_fn=lambda x: x + [item[value_key]]
            )
        return nested_output

    def path(self, path, data):
        """
        Function:

        - Returns the value of a path within a nested dictionary

        Requires:

        - `path`:
            - Type: list of strs | str
            - What: The path to pull given the data
            - Note: If a string is passed, assumes a single item path list with that string
        - `data`:
            - Type: dict
            - What: A dictionary to get the path from

        Example:

        ```
        data={'a':{'b':1}}
        p.path(path=['a','b'], data=data) #=> 1
        ```
        """
        if isinstance(path, str):
            path=[path]
        if len(path) > 0:
            return self.path(data=data[path[0]], path=path[1:])
        return data

    def pathOr(self, default, path, data):
        """
        Function:

        - Returns the value of a path within a nested dictionary or a default value if that path does not exist

        Requires:

        - `default`:
            - Type: any
            - What: The object to return if the path does not exist
        - `path`:
            - Type: list of strs | str
            - What: The path to pull given the data
            - Note: If a string is passed, assumes a single item path list with that string
        - `data`:
            - Type: dict
            - What: A dictionary to get the path from

        Example:

        ```
        data={'a':{'b':1}}
        p.path(default=2, path=['a','c'], data=data) #=> 2
        ```
        """
        if isinstance(path, str):
            path=[path]
        if len(path) > 0:
            if path[0] in data:
                return self.path(data=data[path[0]], path=path[1:])
            else:
                return default
        return data

    def pipe(self, fns, data):
        """
        Function:

        - Pipes data through n functions in order (left to right composition) and returns the output

        Requires:

        - `fns`:
            - Type: list of (functions | methods)
            - What: The list of functions and methods to pipe the data through
            - Notes: The first function in the list can be any arity (accepting any number of inputs)
            - Notes: Any further function in the list can only be unary (single input)
            - Notes: A function can be curried, but is not required to be
            - Notes: You may opt to curry functions and add inputs to make them unary
        - `data`:
            - Type: any
            - What: The data to be piped through the specified `fns`

        Examples:

        ```
        data=['abc','def']
        p.pipe(fns=[p.head, p.tail], data=data) #=> 'c'
        ```

        ```
        data={'a':{'b':'c'}}
        curriedPath=p.curry(p.path)
        p.pipe(fns=[curriedPath('a'), curriedPath('b')], data=data) #=> 'c'
        ```
        """
        if not isinstance(fns, list):
            self.exception('`fns` must be a list')
        if len(fns)==0:
            self.exception('`fns` must be a list with at least one function')
        if self.getArity(fns[0])==0:
            self.exception('The first function in `fns` can have n arity (accepting n args), but this must be greater than 0.')
        if not all([(self.getArity(fn)==1) for fn in fns[1:]]):
            self.exception('Only the first function in `fns` can have n arity (accept n args). All other functions must have an arity of one (accepting one argument).')
        for fn in fns:
            data=fn(data)
        return data

    def pluck(self, path, data):
        """
        Function:

        - Returns the values of a path within a list of nested dictionaries

        Requires:

        - `path`:
            - Type: list of strs
            - What: The path to pull given the data
            - Note: If a string is passed, assumes a single item path list with that string
        - `data`:
            - Type: list of dicts
            - What: A list of dictionaries to get the path from

        Example:

        ```
        data=[{'a':{'b':1, 'c':'d'}},{'a':{'b':2, 'c':'e'}}]
        p.pluck(path=['a','b'], data=data) #=> [1,2]
        ```
        """
        if not isinstance(data, list):
            self.exception("Attempting to pluck from an object that is not a list")
        if len(data) == 0:
            self.exception("Attempting to pluck from an empty list")
        return [self.path(data=i, path=path) for i in data]

    def pluckIf(self, if_path, if_vals, path, data):
        """
        Function:

        - Returns the values of a path within a list of nested dictionaries if a path in those same dictionaries matches a value

        Requires:

        - `if_path`:
            - Type: list of strs
            - What: Path to check if the `if_val` matches
        - `if_vals`:
            - Type: list of any types
            - What: If the `if_path`s value is in this list, this item is returned
            - Note: Items should be the same type as objects at end of `if_path`
        - `path`:
            - Type: list of strs
            - What: The path to pull given the data
            - Note: If a string is passed, assumes a single item path list with that string
        - `data`:
            - Type: list of dicts
            - What: A list of dictionary to get the path from

        Example:

        ```
        data=[{'a':{'b':1, 'c':'d'}},{'a':{'b':2, 'c':'e'}}]
        p.pluck(if_path=['a','c'], if_vals=['d'], path=['a','b'], data=data) #=> [1]
        ```
        """
        if not isinstance(if_vals, list):
            self.exception('`if_vals` must be a list')
        if not isinstance(data, list):
            self.exception("Attempting to pluck from an object that is not a list")
        if len(data) == 0:
            self.exception("Attempting to pluck from an empty list")
        return [self.path(data=i, path=path) for i in data if self.path(data=i, path=if_path) in if_vals]

    def safeDivide(self, denominator, a):
        """
        Function:

        - Forces division to work by enforcing a denominator of 1 if the provided denominator is zero

        Requires:

        - `denominator`:
            - Type: int | float
            - What: The denominator

        - `a`:
            - Type: int | float
            - What: The numerator

        Example:

        ```
        p.safeDivide(2,10) #=> 5
        p.safeDivide(0,10) #=> 10
        ```
        """
        if (
            not isinstance(a, (float, int)) or
            not isinstance(denominator, (float, int))
        ):
            self.exception('`safeDivide` can only be called on `float` or `int` objects')
        return a/denominator if denominator!=0 else a

    def safeDivideDefault(self, default_denominator, denominator, a):
        """
        Function:

        - Forces division to work by enforcing a non zero default denominator if the provided denominator is zero

        Requires:

        - `default_denominator`:
            - Type: int | float
            - What: A non zero denominator to use if denominator is zero
            - Default: 1
        - `denominator`:
            - Type: int | float
            - What: The denominator
        - `a`:
            - Type: int | float
            - What: The numerator

        Example:

        ```
        p.safeDivideDefault(2,5,10) #=> 2
        p.safeDivideDefault(2,0,10) #=> 5
        ```
        """
        if (
            not isinstance(a, (float, int)) or
            not isinstance(denominator, (float, int)) or
            not isinstance(default_denominator, (float, int))
        ):
            self.exception('`safeDivideDefault` can only be called on `float` or `int` objects')
        if default_denominator==0:
            self.exception('`safeDivideDefault` `default_denominator` can not be 0')
        return a/denominator if denominator!=0 else a/default_denominator

    def symmetricDifference(self, a, b):
        """
        Function:

        - Combines two lists into a list of no duplicates items present in one list but not the other

        Requires:

        - `a`:
            - Type: list
            - What: List of items in which to look for a difference
        - `b`:
            - Type: list
            - What: List of items in which to look for a difference

        Example:

        ```
        a=['a','b']
        b=['b','c']
        p.symmetricDifference(a=a, b=b) #=> ['a','c']
        ```
        """
        return list(set(a).difference(set(b)))+list(set(b).difference(set(a)))

    def tail(self, data):
        """
        Function:

        - Picks the last item out of a list or string

        Requires:

        - `data`:
            - Type: list | str
            - What: A list or string

        Example:

        ```
        data=['fe','fi','fo','fum']
        p.first(
            data=data
        ) #=> fum
        ```
        """
        if not isinstance(data, (list,str)):
            self.exception("`tail` can only be called on a `str` or a `list`")
        if not len(data)>0:
            self.exception("Attempting to call `tail` on an empty list or str")
        return data[-1]

    def thunkify(self, fn):
        """
        Function:

        - Creates a curried thunk out of a function
        - Evaluation of the thunk lazy and is delayed until called

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to thunkify
            - Note: Class methods auto apply self during thunkify

        Examples:

        ```
        zipThunk=p.thunkify(p.zip)(['a','b'])([1,2])
        zipThunk() #=> [['a',1],['b',2]]
        ```
        """
        if not isinstance(fn, curry_fn):
            return curry_fn(fn, isThunk=True)
        return fn.thunkify()

    def zip(self, a, b):
        """
        Function:

        - Creates a new list out of the two supplied by pairing up equally-positioned items from both lists

        Requires:

        - `a`:
            - Type: list
            - What: List of items to appear in new list first
        - `b`:
            - Type: list
            - What: List of items to appear in new list second

        Example:

        ```
        a=['a','b']
        b=[1,2]
        p.zip(a=a, b=b) #=> [['a',1],['b',2]]
        ```
        """
        return [list(item) for item in zip(a,b)]

    def zipObj(self, a, b):
        """
        Function:

        - Creates a new dict out of two supplied lists by pairing up equally-positioned items from both lists
        - The first list represents keys and the second values

        Requires:

        - `a`:
            - Type: list
            - What: List of items to appear in new list first
        - `b`:
            - Type: list
            - What: List of items to appear in new list second

        Example:

        ```
        a=['a','b']
        b=[1,2]
        p.zipObj(a=a, b=b) #=> {'a':1, 'b':2}
        ```
        """
        return dict(zip(a,b))
