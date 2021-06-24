from pamda.pamda_utils import pamda_utils

class pamda_class(pamda_utils):
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

    def path(self, data, path, Or=None):
        """
        Function:

        - Returns the value of a path within a nested dictionary

        Requires:

        - `data`:
            - Type: dict
            - What: A dictionary to get the path from
        - `path`:
            - Type: list of strs
            - What: The path to pull given the data

        Example:

        ```
        data={'a':{'b':1}}
        p.path(data=data, path=['a','b']) #=> 1
        ```
        """
        #TODO: Add Or func
        #TODO: Accept string for path if prop
        if len(path) > 0:
            return self.path(data=data[path[0]], path=path[1:])
        return data

    def hasPath(self, data, path):
        """
        Function:

        - Checks if a path exists within a nested dictionary

        Requires:

        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists
        - `path`:
            - Type: list of strs or single str
            - What: The path to check

        Example:

        ```
        data={'a':{'b':1}}
        p.hasPath(data=data, path=['a','b']) #=> True
        p.hasPath(data=data, path=['a','d']) #=> False
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

    def assocPath(self, data, path, value):
        """
        Function:

        - Ensures a path exists within a nested dictionary

        Requires:

        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists
        - `path`:
            - Type: list of strs
            - What: The path to check
        - `value`:
            - Type: any
            - What: The value to appropriate to the end of the path

        Example:

        ```
        data={'a':{'b':1}}
        p.assocPath(data=data, path=['a','c'], value=3) #=> {'a':{'b':1, 'c':3}}
        ```
        """
        if len(path) > 1:
            if path[0] not in data:
                data[path[0]] = {}
            data[path[0]] = self.assocPath(data=data[path[0]], path=path[1:],value=value)
            return data
        else:
            data[path[0]] = value
            return data

    def assocPathComplex(self, data, path, default=None, default_func=lambda x: x):
        """
        Function:

        - Ensures a path exists within a nested dictionary

        Requires:

        - `data`:
            - Type: dict
            - What: A dictionary to check if the path exists
        - `path`:
            - Type: list of strs
            - What: The path to check

        Optional:

        - `default`:
            - Type: any
            - What: The default item to add to a path that does not yet exist
            - Default: None
        - `default_func`:
            - Type: lambda function
            - What: A single input lambda function that takes in the current path item (or default) and adjusts it
            - Default: `lambda x: x` # Returns the value in the dict or the default value if none was present

        Example:

        ```
        data={'a':{'b':1}}
        p.assocPathComplex(data=data, path=['a','b'], default=[]) #=> {'a':{'b':1}}
        p.assocPathComplex(data=data, path=['a','c'], default=[]) #=> {'a':{'b':1, 'c':[]}}
        p.assocPathComplex(data=data, path=['a','d'], default=[2], default_func=lambda x:x+[1]) #=> {'a':{'b':1,'c':[],'d':[2,1]}}
        ```
        """
        if len(path) > 1:
            if path[0] not in data:
                data[path[0]] = {}
            data[path[0]] = self.assocPathComplex(data=data[path[0]], path=path[1:], default=default, default_func=default_func)
            return data
        else:
            if path[0] not in data:
                data[path[0]] = default
            data[path[0]] = default_func(data[path[0]])
            return data

    def dissocPath(self, data, path):
        """
        Function:

        - Removes the value at the end of a path within a nested dictionary

        Requires:

        - `data`:
            - Type: dict
            - What: A dictionary with a path to be removed
        - `path`:
            - Type: list of strs
            - What: The path to remove from the dictionary

        Example:

        ```
        data={'a':{'b':{'c':0,'d':1}}}
        p.dissocPath(data=data, path=['a','b','c']) #=> {'a':{'b':{'d':1}}}
        ```
        """
        if not self.hasPath(data, path):
            self.warn(message="Path does not exist")
            return data
        if len(path)==0:
            return {}
        return self.assocPath(data=data, path=path[:-1], value={key:value for key, value in self.path(data, path=path[:-1]).items() if key!=path[-1]})

    def pluck(self, data, path, if_path=None, if_vals=[]):
        """
        Function:

        - Returns the values of a path within a list of nested dictionaries

        Requires:

        - `data`:
            - Type: list of dicts
            - What: A list of dictionary to get the path from
        - `path`:
            - Type: list of strs
            - What: The path to pull given the data

        Optional:
        - `if_path`:
            - Type: list of strs
            - What: Path to check if the `if_val` matches
            - Default: None
            - Note: If None, no filtering is applied
        - `if_vals`:
            - Type: list of any types
            - What: If the `if_path`s value is in this list, this item is returned
            - Note: Items should be the same type as objects at end of `if_path`
            - Note: If None, no filtering is applied

        Example:

        ```
        data=[{'a':{'b':1, 'c':'d'}},{'a':{'b':2, 'c':'e'}}]
        p.pluck(data=data, path=['a','b']) #=> [1,2]
        p.pluck(data=data, path=['a','b'], if_path=['a','c'], if_vals=['d']) #=> [1]
        ```
        """
        if not isinstance(data, list):
            self.exception("Attempting to pluck from an object that is not a list")
        if len(data) == 0:
            self.exception("Attempting to pluck from an empty list")
        if if_path is not None and isinstance(if_vals, list):
            return [self.path(data=i, path=path) for i in data if self.path(data=i, path=if_path) in if_vals]
        return [self.path(data=i, path=path) for i in data]

    def nest(self, data, nest_by_variables, nest_output_variable):
        """
        Function:

        - Nests a list of dictionaries into a nested dictionary
        - Similar items are appended to a list in the end of the nested dictionary

        Requires:

        - `data`:
            - Type: list of dicts
            - What: A list of dictionaries to use for nesting purposes
        - `nest_by_variables`:
            - Type: list of strs
            - What: The variables to pull from each item in data
            - Note: Used to build out the nested dicitonary
            - Note: Order matters as the nesting occurs in order of variable
        - `nest_output_variable`:
            - Type: str
            - What: The variable to add to the list at the end of the nested dictionary path

        Example:

        ```
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
                path=[item[key] for key in nest_by_variables],
                default=[],
                default_func=lambda x: x + [item[nest_output_variable]]
            )
        return nested_output

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

    def mergeDeep(self, data, update_data):
        """
        Function:

        - Recursively merges two nested dictionaries keeping all keys at each layer
        - Values from `update_data` are used when keys are present in both dictionaries

        Requires:

        - `data`:
            - Type: dict
            - What: The original data that will be merged into

        - `update_data`:
            - Type: dict
            - What

        Example:

        ```
        data={'a':{'b':{'c':'d'},'e':'f'}}
        update_data={'a':{'b':{'h':'i'},'e','g'}}
        p.mergeDeep(
            data=data,
            update_data=update_data
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
        p.intersection(a=a, b=b) #=> ['a']
        ```
        """
        return list(set(a).difference(set(b)))

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
        p.intersection(a=a, b=b) #=> ['a','c']
        ```
        """
        return list(set(a).difference(set(b)))+list(set(b).difference(set(a)))

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
        p.zip(a=a, b=b) #=> {'a':1, 'b':2}
        ```
        """
        return dict(zip(a,b))
