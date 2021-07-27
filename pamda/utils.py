import sys, json, csv

class error:
    def warn(self, message, depth=0):
        """
        Usage:

        - Creates a class based warning message

        Requires:

        - `message`:
            - Type: str
            - What: The message to warn users with
            - Note: Messages with `{class_name}` and `{method_name}` in them are formatted appropriately

        Optional:

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

        Optional:
        
        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0

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

class utils(error):
    ######################
    # Data Handling
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

    ######################
    # Helpful Functions
    def getMethods(self, object):
        """
        Function:

        - Returns the callable methods of a class (dunder-excluded) as a list of strs

        Requires:

        - `object`:
            - Type: any
            - What: Any python object
            - Default: 1

        Example:

        ```
        class MyClass:
            def A(self):
                pass

            def B(self):
                pass


        p.getMethods(MyClass) #=> ['A', 'B']
        ```
        """
        return [fn for fn in dir(object) if callable(getattr(object, fn)) and not fn.startswith("__")]
