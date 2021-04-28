import json, csv, math

class pamda_error:
    def warn(self, message, depth=0):
        """
        Usage:

        - Creates a class based warning message

        Requires:
        - `message`:
            - Type: str
            - What: The message to warn users with
            - Note: Messages with `{class_name}` and `{method_name}` in them are formatted appropriately
        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0

        Notes:

        - If `self.show_warning_stack=True`, also prints the stack trace up to 10 layers deep
        - If `self.show_warnings=False`, supresses all warnings
        """
        if self.__dict__.get('show_warnings',True):
            kwargs={
                'class_name':self.__class__.__name__,
                'method_name':sys._getframe(depth).f_back.f_code.co_name
            }
            pre_message="(Warning for `{class_name}.{method_name}`): ".format(**kwargs)
            # Attempt to format in kwargs where possible
            try:
                message=pre_message+message.format(**kwargs)
            except:
                message=pre_message+message
            if self.__dict__.get('show_warning_stack',False):
                traceback.print_stack(limit=10)
            print(message)

    def vprint(self, message, depth=0, force=False):
        """
        Usage:

        - Print a given statement if `self.verbose` is true

        Requires:

        - `message`:
            - Type: str
            - What: A message to print if `self.verbose` is true
            - Note: Messages with `{{class_name}}` and `{{method_name}}` in them are formatted appropriately

        Optional:

        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0
        - `force`:
            - Type: bool
            - What: Force a print statement even if not in verbose
            - Note: For formatting purposes
            - Default: False
        """
        if self.verbose or force:
            kwargs={
                'class_name':self.__class__.__name__,
                'method_name':sys._getframe(depth).f_back.f_code.co_name
            }
            pre_message="(`{class_name}.{method_name}`): ".format(**kwargs)
            # Attempt to format in kwargs where possible
            try:
                message=pre_message+message.format(**kwargs)
            except:
                message=pre_message+message
            print(message)

    def exception(self, message, depth=0):
        """
        Usage:

        - Creates a class based exception message

        Requires:

        - `message`:
            - Type: str
            - What: The message to warn users with
            - Note: Messages with `{{class_name}}` and `{{method_name}}` in them are formatted appropriately
        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0

        Notes:

        - If `self.show_warning_stack=True`, also prints the stack trace up to 10 layers deep
        - If `self.show_warnings=False`, supresses all warnings
        """
        kwargs={
            'class_name':self.__class__.__name__,
            'method_name':sys._getframe(depth).f_back.f_code.co_name
        }
        pre_message="(Exception for `{class_name}.{method_name}`): ".format(**kwargs)
        # Attempt to format in kwargs where possible
        try:
            message=pre_message+message.format(**kwargs)
        except:
            message=pre_message+message
        raise Exception(message)

class pamda_class(pamda_error):
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

    # def intersection(self):
    #     #TODO Code this
    #     pass
    #
    # def difference(self, type='symmetric'):
    #     #TODO Code this
    #     pass
    #
    # def zipObj(self):
    #     #TODO Code this
    #     pass

class pamdata(pamda_error):
    def read_csv(self, filename, has_header=True, return_dict=True):
        """
        Function:

        - Reads the contents of a csv and converts it to list of dicts or list of lists

        Requires:

        - `filename`:
            - Type: str
            - What: The filepath of the csv to read

        Optional:

        - `has_header`:
            - Type: bool
            - What: Flag to indicate if the csv has an initial row that identifies columns
            - Default: True
            - Note: Returns a list of lists
        - `return_dict`:
            - Type: bool
            - What: Flag to indicate if the csv should be converted to:
                - True: list of dicts
                - False: list of lists
            - Note: If True, requires `has_header` to be True as the header determines the keys of the dicts
        """
        with open(filename) as f:
            file_data = csv.reader(f, delimiter=",", quotechar='"')
            if has_header:
                headers = next(file_data)
            if has_header and return_dict:
                return [dict(zip(headers, i)) for i in file_data]
            elif not has_header and return_dict:
                self.exception(message="If `return_dict` is True, `has_header` must also be True.")
            else:
                return [i for i in file_data]

    def write_csv(self, filename, data):
        """
        Function:

        - Writes the contents of a list of list or list of dicts to a csv

        Requires:

        - `filename`:
            - Type: str
            - What: The filepath of the csv to read
        - `data`:
            - Type: list of lists | list of dicts
            - What: The data to write
        """
        with open(filename, 'w') as f:
            if isinstance(data[0], dict):
                writer=csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            elif isinstance(data[0], list):
                writer=csv.writer(f)
                for row in data:
                    writer.writerow(row)
            else:
                self.exception("write_csv takes in list of lists or list of dicts only.")

    def read_json(self, filename):
        """
        Function:

        - Reads the contents of a json

        Requires:
        - `filename`:
            - Type: str
            - What: The filepath of the json to read
        """
        const_map = {
            '-Infinity': float('-Infinity'),
            'Infinity': float('Infinity'),
            'NaN': None,
        }
        with open(filename) as f:
            return json.load(f, parse_constant=lambda x:const_map[x])

    def write_json(self, filename, data, pretty=False):
        """
        Function:

        - Writes the contents of a list of list or list of dicts to a json

        Requires:

        - `filename`:
            - Type: str
            - What: The filepath of the json to write
        - `data`:
            - Type: A json serializable python object
            - What: The data to write
        """
        with open(filename, 'w') as f:
            if pretty:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f)

pamda=pamda_class()
