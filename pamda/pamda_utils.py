import csv, json
from pamda import pamda_wrappers
import type_enforced


@type_enforced.Enforcer
@pamda_wrappers.staticmethod_wrap
class pamda_utils:
    ######################
    # Data Handling
    def read_csv(
        filename: str, return_dict: bool = True, cast_items:bool = False, cast_dict: [dict, None] = None
    ):
        """
        Function:

        - Reads the contents of a csv and converts it to list of dicts or list of lists
        - Note: The csv must have a header row indicating the names of each column

        Requires:

        - `filename`:
            - Type: str
            - What: The filepath of the csv to read

        Optional:

        - `return_dict`:
            - Type: bool
            - What: Flag to indicate if the csv should be converted to:
                - True: list of dicts (with each key being the associated column header)
                - False: list of lists (with the first row being the headers)
            - Default: True
        - `cast_items`:
            - Type: bool
            - What: Flag to indicate if an attempt to cast each item to a proper type
            - Default: True
            - Note: This is useful for converting strings to ints, floats, etc.
            - Note: This works in conjunction with `cast_dict`
                - If `cast_dict` is not None, then an automated attempt to cast the items will be made
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
        with open(filename) as f:
            file_data = csv.reader(f, delimiter=",", quotechar='"')
            headers = next(file_data)
            if cast_items:
                if cast_dict is not None:
                    def cast(obj, name):
                        return cast_dict.get(name, lambda x: x)(obj)
                else:
                    def cast(obj, name):
                        if not isinstance(obj, str):
                            return obj
                        if obj == "" or obj.lower() == 'none' or obj.lower() == 'null':
                            return None
                        if obj.lower() == "true":
                            return True
                        if obj.lower() == "false":
                            return False
                        try:
                            float_obj = float(obj)
                            return int(float_obj) if float_obj == int(float_obj) else float_obj
                        except:
                            return obj
                data = [{header:cast(item,header) for header, item in zip(headers, row)} for row in file_data]
            else:
                data = [dict(zip(headers, row)) for row in file_data]
            if return_dict:
                return data
            else:
                return [headers]+[list(item.values()) for item in data]

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

    def getForceDict(object: [dict, list], key: [str, int]):
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
        if not isinstance(object.get(key), (dict, list)):
            object.__setitem__(key, {})
        return object.get(key)
