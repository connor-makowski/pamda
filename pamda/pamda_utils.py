import csv, json
from pamda import pamda_wrappers
from pamda.pamda_fast import __getForceDict__
import type_enforced


@type_enforced.Enforcer
@pamda_wrappers.staticmethod_wrap
class pamda_utils:
    ######################
    # Data Handling
    def read_csv(
        filename: str,
        return_dict: bool = True,
        cast_items: bool = True,
        cast_dict: dict | str | None = None,
        return_type: str | None = None,
    ):
        """
        Function:

        - Reads the contents of a csv and converts it to list of dicts or list of lists
        - Note: The csv must have a header row indicating the names of each column

        Requires:

        - `filename`:
            - Type: str
            - What: The filepath of the csv to read
                - Note: The first row of the csv must be the header row

        Optional:

        - `return_dict`:
            - Type: bool
            - What: Flag to indicate if the csv should be converted to:
                - True: list of dicts (with each key being the associated column header)
                - False: list of lists (with the first row being the headers)
            - Default: True
            - Notes:
                - This has been deprecated in favor of `return_type`
                - This has been kept for backwards compatibility
                - If return_type is specified, this will be ignored
        - `return_type`:
            - Type: str
            - Options:
                - `list_of_dicts` (default if `return_dict` is True)
                    - A list of dictionaries with each key being the associated column header
                - `dict_of_lists`
                    - A dictionary of lists with each key being the associated column header and each value being a list of the values in that column
                - `list_of_row_lists`
                    - A list of lists (records) with each row being a list of the values in that row
                    - The first row is the header row
                - `list_of_col_lists`
                    - A list of lists (columns) with each column being a list of the values in that column
                    - The first item in each sublist is the header for that column
        - `cast_items`:
            - Type: bool
            - What: Flag to indicate if an attempt to cast each item to a proper type
            - Default: True
            - Note: This is useful for converting strings to ints, floats, etc.
            - Note: This works in conjunction with `cast_dict`
                - If `cast_dict` is not None, then an automated attempt to cast the items will be made
                - For automated casting, the following rules are applied to each item in the data:
                    - If the item is a string:
                        - If the string is empty, `None` will be returned
                        - If the string is "None" or "null", `None` will be returned
                        - If the string is "True" or "true", `True` will be returned
                        - If the string is "False" or "false", `False` will be returned
                        - If the string is a valid float, the float will be returned
                        - If the string is a valid int, the int will be returned
                        - Otherwise, the string will be returned
                    - If the item is not a string, it will be returned as is
        - `cast_dict`:
            - Type: dict
            - What: A dictionary of functions to cast each column (by name) in the csv
            - Default: None
            - Note: Unspecified column names will be treated as strings
            - Note: `cast_items` must be `True` to use this
            - EG: {
                'user_id': lambda x: int(x),
                'year': lambda x: int(x),
                'pass': lambda x: x.lower()=='true',
            }
        """
        assert return_type in [
            None,
            "list_of_dicts",
            "dict_of_lists",
            "list_of_row_lists",
            "list_of_col_lists",
        ], f"Invalid return_type: {return_type}"
        with open(filename) as f:
            file_data = csv.reader(f, delimiter=",", quotechar='"')
            headers = next(file_data)
            data = list(zip(*[row for row in file_data]))
        if cast_items:
            if cast_dict is not None:
                for idx, header in enumerate(headers):
                    cast_fn = cast_dict.get(header, lambda x: x)
                    data[idx] = [cast_fn(item) for item in data[idx]]
            else:

                def cast(obj):
                    if not isinstance(obj, str):
                        return obj
                    obj_lower = obj.lower()
                    if obj == "" or obj_lower == "none" or obj_lower == "null":
                        return None
                    if obj_lower == "true":
                        return True
                    if obj_lower == "false":
                        return False
                    try:
                        float_obj = float(obj)
                        return (
                            int(float_obj)
                            if float_obj == int(float_obj)
                            else float_obj
                        )
                    except:
                        return obj

                for idx, header in enumerate(headers):
                    data[idx] = [cast(item) for item in data[idx]]
        # Maintain backwards compatibility
        # TODO: Deprecate this in the next major release
        if return_type == None:
            return_type = (
                "list_of_dicts" if return_dict else "list_of_row_lists"
            )
        if return_type == "list_of_dicts":
            return [dict(zip(headers, row)) for row in zip(*data)]
        elif return_type == "dict_of_lists":
            return {header: col for header, col in zip(headers, data)}
        elif return_type == "list_of_row_lists":
            return [headers] + [list(row) for row in zip(*data)]
        elif return_type == "list_of_col_lists":
            return [[header] + list(col) for header, col in zip(headers, data)]

    def write_csv(filename: str, data):
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
        with open(filename, "w") as f:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            elif isinstance(data[0], list):
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
            else:
                raise Exception(
                    "`write_csv` takes in list of lists or list of dicts only."
                )

    def read_json(filename: str):
        """
        Function:

        - Reads the contents of a json

        Requires:
        - `filename`:
            - Type: str
            - What: The filepath of the json to read
        """
        const_map = {
            "-Infinity": float("-Infinity"),
            "Infinity": float("Infinity"),
            "NaN": None,
        }
        with open(filename) as f:
            return json.load(f, parse_constant=lambda x: const_map[x])

    def write_json(filename: str, data, pretty: bool = False):
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
        with open(filename, "w") as f:
            if pretty:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f)

    ######################
    # Helpful Functions
    def getMethods(object):
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


        pamda.getMethods(MyClass) #=> ['A', 'B']
        ```
        """
        return [
            fn
            for fn in dir(object)
            if callable(getattr(object, fn)) and not fn.startswith("__")
        ]

    def getForceDict(object: dict | list, key: str | int | tuple):
        """
        Function:

        - Returns a value from a dictionary (or list) given a key (or index)  and forces that value to be a dictionary if it is not a dictionary (or a list)
        - Note: This updates the object in place to force the value from the key to be a dictionary

        Requires:

        - `object`:
            - Type: dict | list
            - What: The object from which to look for a key or index
        - `key`:
            - Type: str | int
            - What: The key or index to look up in the object

        Example:

        ```
        data = {'a':{}, 'b':1, 'c':[]}

        pamda.getForceDict(data, 'a') #=> {}
        pamda.getForceDict(data, 'b') #=> {}
        pamda.getForceDict(data, 'c') #=> []

        # Note that the object has been updated in place
        data #=> {'a':{}, 'b':{}, 'c':[]}
        ```
        """
        # TODO: Remove this function in future major release as it is now located in pamda_fast
        return __getForceDict__(object, key)
