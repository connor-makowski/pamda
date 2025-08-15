from functools import reduce
from pamda.pamda_utils import pamda_utils
from pamda.pamda_fast import (
    __getForceDict__,
    __assocPath__,
    __groupByHashable__,
    __mergeDeep__,
    __pathOr__,
    __getKeyValues__,
)
from pamda.pamda_curry import curry_obj
from pamda import pamda_wrappers
from typing import Any


@pamda_wrappers.typed_curry_wrap
@pamda_wrappers.classmethod_wrap
class pamda(pamda_utils):
    def accumulate(self, fn, initial_accumulator, data: list):
        """
        Function:

        - Returns an accumulated list of items by iterating a function starting with an accumulator over a list

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to reduce
            - Note: This function should have an arity of 2 (take two inputs)
            - Note: The first input should take the accumulator value
            - Note: The second input should take the data value
        -`initial_accumulator`:
            - Type: any
            - What: The initial item to pass into the function when starting the accumulation process
        - `data`:
            - Type: list
            - What: The list of items to iterate over

        Example:

        ```
        data=[1,2,3,4]
        pamda.accumulate(
            fn=pamda.add,
            initial_accumulator=0,
            data=data
        )
        #=> [1,3,6,10]

        ```
        """
        fn = self.curry(fn)
        if fn.__arity__ != 2:
            raise Exception("`fn` must have an arity of 2 (take two inputs)")
        if not len(data) > 0:
            raise Exception(
                "`data` has a length of 0, however it must have a length of at least 1"
            )
        acc = initial_accumulator
        out = []
        for i in data:
            acc = fn(acc, i)
            out.append(acc)
        return out

    def add(self, a: int | float, b: int | float):
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
        pamda.add(1, 2) #=> 3
        ```
        """
        return a + b

    def adjust(self, index: int, fn, data: list):
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
        pamda.adjust(
            index=1,
            fn=pamda.inc,
            data=data
        ) #=> [1,6,9]
        ```
        """
        fn = self.curry(fn)
        index = self.clamp(-len(data), len(data) - 1, index)
        data[index] = fn(data[index])
        return data

    def assocPath(self, path: list | str | int | tuple, value, data: dict):
        """
        Function:

        - Ensures a path exists within a nested dictionary
        - Note: This updates the object in place, but also returns the object

        Requires:

        - `path`:
            - Type: list[str | int | tuple] | str | int | tuple
            - What: The path to check
            - Note: If a string is passed, assumes a single item path list with that string
        - `value`:
            - Type: any
            - What: The value to appropriate to the end of the path
        - `data`:
            - Type: dict
            - What: A dictionary in which to associate the given value to the given path

        Example:

        ```
        data={'a':{'b':1}}
        pamda.assocPath(path=['a','c'], value=3, data=data) #=> {'a':{'b':1, 'c':3}}
        ```
        """
        if not isinstance(path, list):
            path = [path]
        reduce(__getForceDict__, path[:-1], data).__setitem__(path[-1], value)
        return data

    def assocPathComplex(
        self, default, default_fn, path: list | int | float | tuple, data: dict
    ):
        """
        Function:

        - Ensures a path exists within a nested dictionary
        - Note: This updates the object in place, but also returns the object

        Requires:

        - `default`:
            - Type: any
            - What: The default item to add to a path that does not yet exist
        - `default_fn`:
            - Type: function | method
            - What: A unary (single input) function that takes in the current path item (or default) and adjusts it
            - Example: `lambda x: x` # Returns the value in the dict or the default value if none was present
        - `path`:
            - Type: list[str | int | tuple] | str | int | tuple
            - What: The path to check
        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists

        Example:

        ```
        data={'a':{'b':1}}
        pamda.assocPathComplex(default=[2], default_fn=lambda x:x+[1], path=['a','c'], data=data) #=> {'a':{'b':1,'c':[2,1]}}
        ```
        """
        if self.getArity(default_fn) != 1:
            raise Exception(
                "`assocPathComplex` `default_fn` must be an unary (single input) function."
            )
        if not isinstance(path, list):
            path = [path]
        path_object = reduce(__getForceDict__, path[:-1], data)
        path_object.__setitem__(
            path[-1], default_fn(path_object.get(path[-1], default))
        )
        return data

    def asyncKill(self, fn: curry_obj):
        """
        Function:

        - Kills an asynchronous function that is currently running
        - Returns:
            - `None` if the function has not yet finished running
            - The result of the function if it has finished running

        Requires:

        - `fn`:
            - Type: thunkified function | thunkified method
            - What: The function or method to run asychronously
            - Note: The supplied `fn` must already be asynchronously running

        Notes:

        - See also `asyncRun` and `asyncWait`
        - A thunkified function currently running asynchronously can call `asyncKill` on itself
        - If a function has already finished running, calling `asyncKill` on it will have no effect
        - `asyncKill` does not kill threads that are sleeping (EG: `time.sleep`), but will kill the thread once the sleep is finished

        Example:

        ```
        import time
        from pamda import pamda

        @pamda.thunkify
        def test(name, wait):
            waited = 0
            while waited < wait:
                time.sleep(1)
                waited += 1
                print(f'{name} has waited {waited} seconds')

        async_test = pamda.asyncRun(test('a',3))
        time.sleep(1)
        pamda.asyncKill(async_test)
        # Alternatively:
        # async_test.asyncKill()
        ```
        """
        return fn.asyncKill()

    def asyncRun(self, fn: curry_obj):
        """
        Function:

        - Runs the supplied function asychronously

        Requires:

        - `fn`:
            - Type: thunkified function | thunkified method
            - What: The function or method to run asychronously
            - Note: The supplied `fn` must have an arity of 0

        Notes:

        - To pass inputs to a function in asyncRun, first thunkify the function and pass all arguments before calling `asyncRun` on it
        - To get the results of an `asyncRun` call `asyncWait`
        - To kill an `asyncRun` mid process call `asyncKill`
        - A thunkified function with arity of 0 can call `asyncRun` on itself

        Examples:

        Input:
        ```
        import time

        @pamda.thunkify
        def test(name, wait):
            print(f'{name} start')
            time.sleep(wait)
            print(f'{name} end')

        async_test = pamda.asyncRun(test('a',2))
        sync_test = test('b',1)()
        ```
        Output:
        ```
        a start
        b start
        b end
        a end
        ```


        Input:
        ```
        import time

        @pamda.thunkify
        def test(name, wait):
            time.sleep(wait)
            return f"{name}: {wait}"

        async_test = pamda.asyncRun(test('a',2))
        print(async_test.asyncWait()) #=> a: 2
        ```


        Input:
        ```
        import time

        @pamda.thunkify
        def test(name, wait):
            time.sleep(wait)
            return f"{name}: {wait}"

        async_test = test('a',2).asyncRun()
        print(async_test.asyncWait()) #=> a: 2
        ```
        """
        return fn.asyncRun()

    def asyncWait(self, fn: curry_obj):
        """
        Function:

        - Waits for a supplied function (if needed) and returns the results

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method for which to wait
            - Note: The supplied `fn` must have previously called `asyncRun`

        Notes:

        - A thunkified function that has called `asyncRun` can call `asyncWait` on itself

        Examples:

        ```
        import time

        @pamda.thunkify
        def test(name, wait):
            time.sleep(wait)
            return f"{name}: {wait}"

        async_test = pamda.asyncRun(test('a',2))
        print(pamda.asyncWait(async_test)) #=> a: 2
        ```


        ```
        import time

        @pamda.thunkify
        def test(name, wait):
            time.sleep(wait)
            return f"{name}: {wait}"

        async_test = pamda.asyncRun(test('a',2))
        print(async_test.asyncWait()) #=> a: 2
        ```
        """
        return fn.asyncWait()

    def clamp(self, minimum: int | float, maximum: int | float, a: int | float):
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
        pamda.clamp(1, 3, 2) #=> 2
        pamda.clamp(1, 3, 5) #=> 3
        ```
        """
        return min(max(a, minimum), maximum)

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

        - Once curried, the function | method becomes a curry_obj object
        - The initial function is only called once all inputs are passed


        Examples:

        ```
        curriedZip=pamda.curry(pamda.zip)
        curriedZip(['a','b'])([1,2]) #=> [['a',1],['b',2]]

        # Curried functions can be thunkified at any time
        # See also thunkify
        zipThunk=curriedZip.thunkify()(['a','b'])([1,2])
        zipThunk() #=> [['a',1],['b',2]]
        ```

        ```
        def myFunction(a,b,c):
            return [a,b,c]

        curriedMyFn=pamda.curry(myFunction)

        curriedMyFn(1,2,3) #=> [1,2,3]
        curriedMyFn(1)(2,3) #=> [1,2,3]

        x=curriedMyFn(1)(2)
        x(3) #=> [1,2,3]
        x(4) #=> [1,2,4]


        ```
        """
        if fn.__dict__.get("__isCurried__"):
            return fn()
        return curry_obj(fn)

    def curryTyped(self, fn):
        """
        Function:

        - Curries a function such that inputs can be added interatively and function annotations are type checked at runtime

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to curry
            - Note: Class methods auto apply self during curry

        Notes:

        - Once curried, the function | method becomes a curry_obj object
        - The initial function is only called once all inputs are passed


        Examples:

        ```
        @pamda.curryTyped
        def add(a:int,b:int):
            return a+b

        add(1)(1) #=> 2
        add(1)(1.5) #=> Raises type exception
        ```
        """
        if fn.__dict__.get("__isCurried__"):
            return fn().typeEnforce()
        return curry_obj(fn).typeEnforce()

    def dec(self, a: int | float):
        """
        Function:

        - Decrements a number by one

        Requires:

        - `a`:
            - Type: int | float
            - What: The number to decrement

        Example:

        ```
        pamda.dec(42) #=> 41
        ```
        """
        if not isinstance(a, (int, float)):
            raise Exception("`a` must be an `int` or a `float`")
        return a - 1

    def difference(self, a: list, b: list):
        """
        Function:

        - Combines two lists into a list of no duplicate items present in the first list but not the second

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
        pamda.difference(a=a, b=b) #=> ['a']
        pamda.difference(a=b, b=a) #=> ['c']
        ```
        """
        return list(set(a).difference(set(b)))

    def dissocPath(self, path: list | str | int | tuple, data: dict):
        """
        Function:

        - Removes the value at the end of a path within a nested dictionary
        - Note: This updates the object in place, but also returns the object

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
        pamda.dissocPath(path=['a','b','c'], data=data) #=> {'a':{'b':{'d':1}}}
        ```
        """
        if not isinstance(path, list):
            path = [path]
        if not self.hasPath(path=path, data=data):
            raise Exception("Path does not exist")
        else:
            reduce(__getForceDict__, path[:-1], data).pop(path[-1])
        return data

    def flatten(self, data: list):
        """
        Function:

        - Flattens a list of lists of lists ... into a single list depth first

        Requires:

        - `data`:
            - Type: list of lists
            - What: The list of lists to reduce to a single list
        Example:

        ```
        data=[['a','b'],[1,[2]]]
        pamda.flatten(data=data) #=> ['a','b',1,2]
        ```
        """

        def iter_flatten(data):
            out = []
            for i in data:
                if isinstance(i, list):
                    out.extend(iter_flatten(i))
                else:
                    out.append(i)
            return out

        return iter_flatten(data)

    def flip(self, fn):
        """
        Function:

        - Returns a new function equivalent to the supplied function except that the first two inputs are flipped

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to flip
            - Note: This function must have an arity of at least 2 (take two inputs)
            - Note: Only args are flipped, kwargs are passed as normal

        Notes:

        - Input functions are not flipped in place
        - The returned function is a flipped version of the input function
        - A curried function can be flipped in place by calling fn.flip()
        - A function can be flipped multiple times:
            - At each flip, the first and second inputs for the function as it is currently curried are switched
            - Flipping a function two times before adding an input will return the initial value

        Examples:

        ```
        def concat(a,b,c,d):
            return str(a)+str(b)+str(c)+str(d)

        flip_concat=pamda.flip(concat)

        concat('fe-','fi-','fo-','fum') #=> 'fe-fi-fo-fum'
        flip_concat('fe-','fi-','fo-','fum') #=> 'fi-fe-fo-fum'
        ```

        ```
        @pamda.curry
        def concat(a,b,c,d):
            return str(a)+str(b)+str(c)+str(d)

        concat('fe-','fi-','fo-','fum') #=> 'fe-fi-fo-fum'

        concat.flip()

        concat('fe-','fi-','fo-','fum') #=> 'fi-fe-fo-fum'
        ```

        ```
        @pamda.curry
        def concat(a,b,c,d):
            return str(a)+str(b)+str(c)+str(d)

        a=pamda.flip(concat)('fi-')
        b=pamda.flip(a)('fo-')
        c=pamda.flip(b)('fum')
        c('fe-') #=> 'fe-fi-fo-fum'
        ```

        ```
        def concat(a,b,c,d):
            return str(a)+str(b)+str(c)+str(d)

        a=pamda.flip(concat)('fi-').flip()('fo-').flip()('fum')
        a('fe-') #=> 'fe-fi-fo-fum'
        ```
        """
        fn = self.curry(fn)
        return fn.flip()

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
        pamda.getArity(pamda.zip) #=> 2
        curriedZip=pamda.curry(pamda.zip)
        ABCuriedZip=curriedZip(['a','b'])
        pamda.getArity(ABCuriedZip) #=> 1
        ```
        """
        fn = self.curry(fn)
        return fn.__arity__

    def groupBy(self, fn, data: list):
        """
        Function:

        - Splits a list into a dictionary of sublists keyed by the return string of a provided function

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to group by
            - Note: Must return a string (or other hashable object)
            - Note: This function must be unary (take one input)
            - Note: This function is applied to each item in the list recursively
        - `data`:
            - Type: list
            - What: List of items to apply the function to and then group by the results

        Examples:

        ```
        def getGrade(item):
            score=item['score']
            if score>90:
                return 'A'
            elif score>80:
                return 'B'
            elif score>70:
                return 'C'
            elif score>60:
                return 'D'
            else:
                return 'F'

        data=[
            {'name':'Connor', 'score':75},
            {'name':'Fred', 'score':79},
            {'name':'Joe', 'score':84},
        ]
        pamda.groupBy(getGrade,data)
        #=>{
        #=>    'B':[{'name':'Joe', 'score':84}]
        #=>    'C':[{'name':'Connor', 'score':75},{'name':'Fred', 'score':79}]
        #=>}
        ```
        """
        curried_fn = self.curry(fn)
        if curried_fn.__arity__ != 1:
            raise Exception(
                "groupBy `fn` must only take one parameter as its input"
            )
        return __groupByHashable__(fn=fn, data=data)

    def groupKeys(self, keys: list, data: list):
        """
        Function:

        - Splits a list of dicts into a list of sublists of dicts separated by values with equal keys

        Requires:

        - `keys`:
            - Type: list of strs
            - What: The keys to group by
        - `data`:
            - Type: list of dicts
            - What: List of dictionaries with which to match keys

        Examples:

        ```
        data=[
            {'color':'red', 'size':9, 'shape':'ball'},
            {'color':'red', 'size':10, 'shape':'ball'},
            {'color':'green', 'size':11, 'shape':'ball'},
            {'color':'green', 'size':12, 'shape':'square'}
        ]
        pamda.groupKeys(['color','shape'],data)
        #=> [
        #=>     [{'color': 'red', 'size': 9, 'shape': 'ball'}, {'color': 'red', 'size': 10, 'shape': 'ball'}],
        #=>     [{'color': 'green', 'size': 11, 'shape': 'ball'}],
        #=>     [{'color': 'green', 'size': 12, 'shape': 'square'}]
        #=> ]
        ```
        """

        def key_fn(item):
            return tuple([item[key] for key in keys])

        return list(__groupByHashable__(key_fn, data).values())

    def groupWith(self, fn, data: list):
        """
        Function:

        - Splits a list into a list of sublists where each sublist is determined by adjacent pairwise comparisons from a provided function

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to groub with
            - Note: Must return a boolean value
            - Note: This function must have an arity of two (take two inputs)
            - Note: This function is applied to each item plus the next adjacent item in the list recursively
        - `data`:
            - Type: list
            - What: List of items to apply the function to and then group the results

        Examples:

        ```
        def areEqual(a,b):
            return a==b

        data=[1,2,3,1,1,2,2,3,3,3]
        pamda.groupWith(areEqual,data) #=> [[1], [2], [3], [1, 1], [2, 2], [3, 3, 3]]
        ```
        """
        curried_fn = self.curry(fn)
        if curried_fn.__arity__ != 2:
            raise Exception("groupWith `fn` must take exactly two parameters")
        previous = data[0]
        output = []
        sublist = [previous]
        for i in data[1:]:
            if fn(i, previous):
                sublist.append(i)
            else:
                output.append(sublist)
                sublist = [i]
            previous = i
        output.append(sublist)
        return output

    def hasPath(self, path: list | str, data: dict):
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
        pamda.hasPath(path=['a','b'], data=data) #=> True
        pamda.hasPath(path=['a','d'], data=data) #=> False
        ```
        """
        if isinstance(path, str):
            path = [path]
        return path[-1] in reduce(lambda x, y: x.get(y, {}), path[:-1], data)

    def hardRound(self, decimal_places: int, a: int | float):
        """
        Function:

        - Rounds to a set number of decimal places regardless of floating point math in python

        Requires:

        - `decimal_places`:
            - Type: int
            - What: The number of decimal places to round to
            - Default: 0
            - Notes: Negative numbers accepted (EG -1 rounds to the nearest 10)
        - `a`:
            - Type: int | float
            - What: The number to round

        Example:

        ```
        a=12.345
        pamda.hardRound(1,a) #=> 12.3
        pamda.hardRound(-1,a) #=> 10
        ```
        """
        return int(a * (10**decimal_places) + 0.5) / (10**decimal_places)

    def head(self, data: list | str):
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
        pamda.first(
            data=data
        ) #=> fe
        ```
        """
        if not isinstance(data, (list, str)):
            raise Exception("`head` can only be called on a `str` or a `list`")
        if not len(data) > 0:
            raise Exception("Attempting to call `head` on an empty list or str")
        return data[0]

    def inc(self, a: int | float):
        """
        Function:

        - Increments a number by one

        Requires:

        - `a`:
            - Type: int | float
            - What: The number to increment

        Example:

        ```
        pamda.inc(42) #=> 43
        ```
        """
        if not isinstance(a, (int, float)):
            raise Exception("`a` must be an `int` or a `float`")
        return a + 1

    def intersection(self, a: list, b: list):
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
        pamda.intersection(a=a, b=b) #=> ['b']
        ```
        """
        return list(set(a).intersection(set(b)))

    def map(self, fn, data: list | dict):
        """
        Function:

        - Maps a function over a list or a dictionary

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to map over the list or dictionary
            - Note: This function should have an arity of 1
        - `data`:
            - Type: list | dict
            - What: The list or dict of items to map the function over

        Examples:

        ```
        data=[1,2,3]
        pamda.map(
            fn=pamda.inc,
            data=data
        )
        #=> [2,3,4]
        ```

        ```
        data={'a':1,'b':2,'c':3}
        pamda.map(
            fn=pamda.inc,
            data=data
        )
        #=> {'a':2,'b':3,'c':4}
        ```

        """
        # TODO: Check for efficiency gains
        fn = self.curry(fn)
        if fn.__arity__ != 1:
            raise Exception("`map` `fn` must be unary (take one input)")
        if not len(data) > 0:
            raise Exception(
                "`map` `data` has a length of 0 or is an empty dictionary, however it must have at least one element in it"
            )
        if isinstance(data, dict):
            return {key: fn(value) for key, value in data.items()}
        else:
            return [fn(i) for i in data]

    def mean(self, data: list):
        """
        Function:

        - Calculates the mean of a given list

        Requires:

        - `data`:
            - Type: list of (floats | ints)
            - What: The list with wich to calculate the mean
            - Note: If the length of this list is 0, returns None

        Example:

        ```
        data=[1,2,3]
        pamda.mean(data=data)
        #=> 2
        ```

        ```
        data=[]
        pamda.mean(data=data)
        #=> None
        ```
        """
        if len(data) == 0:
            return None
        return sum(data) / len(data)

    def median(self, data: list):
        """
        Function:

        - Calculates the median of a given list
        - If the length of the list is even, calculates the mean of the two central values

        Requires:

        - `data`:
            - Type: list of (floats | ints)
            - What: The list with wich to calculate the mean
            - Note: If the length of this list is 0, returns None

        Examples:

        ```
        data=[7,2,8,9]
        pamda.median(data=data)
        #=> 7.5
        ```

        ```
        data=[7,8,9]
        pamda.median(data=data)
        #=> 8
        ```

        ```
        data=[]
        pamda.median(data=data)
        #=> None
        ```
        """
        if not isinstance(data, (list)):
            raise Exception("`median` `data` must be a list")
        length = len(data)
        if length == 0:
            return None
        data = sorted(data)
        if length % 2 == 0:
            return (data[int(length / 2)] + data[int(length / 2) - 1]) / 2
        return data[int(length / 2)]

    def mergeDeep(self, update_data, data):
        """
        Function:

        - Recursively merges two nested dictionaries keeping all keys at each layer
        - Values from `update_data` are used when keys are present in both dictionaries

        Requires:

        - `update_data`:
            - Type: any
            - What: The new data that will take precedence during merging
        - `data`:
            - Type: any
            - What: The original data that will be merged into

        Example:

        ```
        data={'a':{'b':{'c':'d'},'e':'f'}}
        update_data={'a':{'b':{'h':'i'},'e':'g'}}
        pamda.mergeDeep(
            update_data=update_data,
            data=data
        ) #=> {'a':{'b':{'c':'d','h':'i'},'e':'g'}}
        ```
        """
        return __mergeDeep__(update_data, data)

    def nest(self, path_keys: list, value_key: str, data: list):
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
        pamda.nest(
            path_keys=['x_1','x_2'],
            value_key='output',
            data=data
        ) #=> {'a':{'b':['c','d'], 'e':['f']}}
        ```
        """
        if not isinstance(data, list):
            raise Exception("Attempting to `nest` an object that is not a list")
        if len(data) == 0:
            raise Exception("Attempting to `nest` from an empty list")
        nested_output = {}
        for item in self.groupKeys(keys=path_keys, data=data):
            nested_output = __assocPath__(
                path=__getKeyValues__(path_keys, item[0]),
                value=[i.get(value_key) for i in item],
                data=nested_output,
            )
        return nested_output

    def nestItem(self, path_keys: list, data: list):
        """
        Function:

        - Nests a list of dictionaries into a nested dictionary
        - Similar items are appended to a list in the end of the nested dictionary
        - Similar to `nest`, except no values are plucked for the aggregated list

        Requires:

        - `path_keys`:
            - Type: list of strs
            - What: The variables to pull from each item in data
            - Note: Used to build out the nested dicitonary
            - Note: Order matters as the nesting occurs in order of variable
        - `data`:
            - Type: list of dicts
            - What: A list of dictionaries to use for nesting purposes

        Example:

        ```
        data=[
            {'x_1':'a','x_2':'b'},
            {'x_1':'a','x_2':'b'},
            {'x_1':'a','x_2':'e'}
        ]
        pamda.nestItem
            path_keys=['x_1','x_2'],
            data=data
        )
        #=> {'a': {'b': [{'x_1': 'a', 'x_2': 'b'}, {'x_1': 'a', 'x_2': 'b'}], 'e': [{'x_1': 'a', 'x_2': 'e'}]}}

        ```
        """
        if not isinstance(data, list):
            raise Exception("Attempting to `nest` an object that is not a list")
        if len(data) == 0:
            raise Exception("Attempting to `nest` from an empty list")
        nested_output = {}
        for item in self.groupKeys(keys=path_keys, data=data):
            nested_output = __assocPath__(
                path=__getKeyValues__(path_keys, item[0]),
                value=item,
                data=nested_output,
            )
        return nested_output

    def path(self, path: list | str, data: dict):
        """
        Function:

        - Returns the value of a path within a nested dictionary or None if the path does not exist

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
        pamda.path(path=['a','b'], data=data) #=> 1
        ```
        """
        if isinstance(path, str):
            path = [path]
        return __pathOr__(None, path, data)

    def pathOr(self, default, path: list | str, data: dict):
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
        pamda.path(default=2, path=['a','c'], data=data) #=> 2
        ```
        """
        if isinstance(path, str):
            path = [path]
        return reduce(lambda x, y: x.get(y, {}), path[:-1], data).get(
            path[-1], default
        )

    def pipe(self, fns: list, args: tuple, kwargs: dict):
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
        - `args`:
            - Type: tuple
            - What: a tuple of positional arguments to pass to the first function in `fns`
        - `kwargs`:
            - Type: dict
            - What: a dictionary of keyword arguments to pass to the first function in `fns`

        Examples:

        ```
        data=['abc','def']
        pamda.pipe(fns=[pamda.head, pamda.tail], args=(data), kwargs={}) #=> 'c'
        pamda.pipe(fns=[pamda.head, pamda.tail], args=(), kwargs={'data':data}) #=> 'c'
        ```

        ```
        data={'a':{'b':'c'}}
        curriedPath=pamda.curry(pamda.path)
        pamda.pipe(fns=[curriedPath('a'), curriedPath('b')], args=(), kwargs={'data':data}) #=> 'c'
        ```
        """
        if len(fns) == 0:
            raise Exception("`fns` must be a list with at least one function")
        if self.getArity(fns[0]) == 0:
            raise Exception(
                "The first function in `fns` can have n arity (accepting n args), but this must be greater than 0."
            )
        if not all([(self.getArity(fn) == 1) for fn in fns[1:]]):
            raise Exception(
                "Only the first function in `fns` can have n arity (accept n args). All other functions must have an arity of one (accepting one argument)."
            )
        out = fns[0](*args, **kwargs)
        for fn in fns[1:]:
            out = fn(out)
        return out

    def pivot(self, data: list[dict] | dict[Any, list]):
        """
        Function:

        - Pivots a list of dictionaries into a dictionary of lists
        - Pivots a dictionary of lists into a list of dictionaries

        Requires:

        - `data`:
            - Type: list of dicts | dict of lists
            - What: The data to pivot
            - Note: If a list of dictionaries is passed, all dictionaries must have the same keys
            - Note: If a dictionary of lists is passed, all lists must have the same length

        Example:

        ```
        data=[
            {'a':1,'b':2},
            {'a':3,'b':4}
        ]
        pamda.pivot(data=data) #=> {'a':[1,3],'b':[2,4]}

        data={'a':[1,3],'b':[2,4]}
        pamda.pivot(data=data)
        #=> [
        #=>     {'a':1,'b':2},
        #=>     {'a':3,'b':4}
        #=> ]
        ```
        """
        if isinstance(data, list):
            return {
                key: [record[key] for record in data] for key in data[0].keys()
            }
        else:
            return [
                {key: data[key][i] for key in data.keys()}
                for i in range(len(data[list(data.keys())[0]]))
            ]

    def pluck(self, path: list | str, data: list):
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
        pamda.pluck(path=['a','b'], data=data) #=> [1,2]
        ```
        """
        if len(data) == 0:
            raise Exception("Attempting to pluck from an empty list")
        if isinstance(path, str):
            path = [path]
        return [__pathOr__(default=None, path=path, data=i) for i in data]

    def pluckIf(self, fn, path: list | str, data: list):
        """
        Function:

        - Returns the values of a path within a list of nested dictionaries if a path in those same dictionaries matches a value

        Requires:

        - `fn`:
            - Type: function
            - What: A function to take in each item in data and return a boolean
            - Note: Only items that return true are plucked
            - Note: Should be a unary function (take one input)
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
        pamda.pluck(fn:lambda x: x['a']['b']==1, path=['a','c'], data=data) #=> ['d']
        ```
        """
        if len(data) == 0:
            raise Exception("Attempting to pluck from an empty list")
        curried_fn = self.curry(fn)
        if curried_fn.__arity__ != 1:
            raise Exception(
                "`pluckIf` `fn` must have an arity of 1 (take one input)"
            )
        if isinstance(path, str):
            path = [path]
        return [
            __pathOr__(default=None, path=path, data=i) for i in data if fn(i)
        ]

    def project(self, keys: list[str], data: list[dict]):
        """
        Function:

        - Returns a list of dictionaries with only the keys provided
        - Analogous to SQL's `SELECT` statement

        Requires:

        - `keys`:
            - Type: list of strs
            - What: The keys to select from each dictionary in the data list
        - `data`:
            - Type: list of dicts
            - What: The list of dictionaries to select from

        Example:

        ```
        data=[
            {'a':1,'b':2,'c':3},
            {'a':4,'b':5,'c':6}
        ]
        pamda.project(keys=['a','c'], data=data)
        #=> [
        #=>     {'a':1,'c':3},
        #=>     {'a':4,'c':6}
        #=> ]
        ```
        """
        return [{key: record[key] for key in keys} for record in data]

    def props(self, keys: list[str], data: dict):
        """
        Function:

        - Returns the values of a list of keys within a dictionary

        Requires:

        - `keys`:
            - Type: list of strs
            - What: The keys to pull given the data
        - `data`:
            - Type: dict
            - What: A dictionary to get the keys from

        Example:
        ```
        data={'a':1,'b':2,'c':3}
        pamda.props(keys=['a','c'], data=data)
        #=> [1,3]
        ```
        """
        return [data[key] for key in keys]

    def reduce(self, fn, initial_accumulator, data: list):
        """
        Function:

        - Returns a single item by iterating a function starting with an accumulator over a list

        Requires:

        - `fn`:
            - Type: function | method
            - What: The function or method to reduce
            - Note: This function should have an arity of 2 (take two inputs)
            - Note: The first input should take the accumulator value
            - Note: The second input should take the data value
        -`initial_accumulator`:
            - Type: any
            - What: The initial item to pass into the function when starting the accumulation process
        - `data`:
            - Type: list
            - What: The list of items to iterate over

        Example:

        ```
        data=[1,2,3,4]
        pamda.reduce(
            fn=pamda.add,
            initial_accumulator=0,
            data=data
        )
        #=> 10

        ```
        """
        fn = self.curry(fn)
        if fn.__arity__ != 2:
            raise Exception(
                "`reduce` `fn` must have an arity of 2 (take two inputs)"
            )
        if not isinstance(data, (list)):
            raise Exception("`reduce` `data` must be a list")
        if not len(data) > 0:
            raise Exception(
                "`reduce` `data` has a length of 0, however it must have a length of at least 1"
            )
        acc = initial_accumulator
        for i in data:
            acc = fn(acc, i)
        return acc

    def safeDivide(self, denominator: int | float, a: int | float):
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
        pamda.safeDivide(2,10) #=> 5
        pamda.safeDivide(0,10) #=> 10
        ```
        """
        return a / denominator if denominator != 0 else a

    def safeDivideDefault(
        self,
        default_denominator: int | float,
        denominator: int | float,
        a: int | float,
    ):
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
        pamda.safeDivideDefault(2,5,10) #=> 2
        pamda.safeDivideDefault(2,0,10) #=> 5
        ```
        """
        if default_denominator == 0:
            raise Exception(
                "`safeDivideDefault` `default_denominator` can not be 0"
            )
        return a / denominator if denominator != 0 else a / default_denominator

    def symmetricDifference(self, a: list, b: list):
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
        pamda.symmetricDifference(a=a, b=b) #=> ['a','c']
        ```
        """
        return list(set(a).difference(set(b))) + list(set(b).difference(set(a)))

    def tail(self, data: list | str):
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
        pamda.tail(
            data=data
        ) #=> fum
        ```
        """
        if not len(data) > 0:
            raise Exception("Attempting to call `tail` on an empty list or str")
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
            - Note: Thunkified functions are automatically curried
            - Note: Class methods auto apply self during thunkify

        Notes:

        - Input functions are not thunkified in place
        - The returned function is a thunkified version of the input function
        - A curried function can be thunkified in place by calling fn.thunkify()

        Examples:

        ```
        def add(a,b):
            return a+b

        addThunk=pamda.thunkify(add)

        add(1,2) #=> 3
        addThunk(1,2)
        addThunk(1,2)() #=> 3

        x=addThunk(1,2)
        x() #=> 3
        ```

        ```
        @pamda.curry
        def add(a,b):
            return a+b

        add(1,2) #=> 3

        add.thunkify()

        add(1,2)
        add(1,2)() #=> 3
        ```
        """
        fn = self.curry(fn)
        return fn.thunkify()

    def unnest(self, data: list):
        """
        Function:

        - Removes one level of depth for all items in a list

        Requires:

        - `data`:
            - Type: list
            - What: A list of items to unnest by one level

        Examples:

        ```
        data=['fe','fi',['fo',['fum']]]
        pamda.unnest(
            data=data
        ) #=> ['fe','fi','fo',['fum']]
        ```
        """
        if not len(data) > 0:
            raise Exception("Attempting to call `unnest` on an empty list")
        output = []
        for i in data:
            if isinstance(i, list):
                output += i
            else:
                output.append(i)
        return output

    def zip(self, a: list, b: list):
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
        pamda.zip(a=a, b=b) #=> [['a',1],['b',2]]
        ```
        """
        return list(map(list, zip(a, b)))

    def zipObj(self, a: list, b: list):
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
        pamda.zipObj(a=a, b=b) #=> {'a':1, 'b':2}
        ```
        """
        return dict(zip(a, b))
