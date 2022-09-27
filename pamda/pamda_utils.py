import csv
import json
from pamda import pamda_wrappers


@pamda_wrappers.staticmethod_wrap
class pamda_utils:
    ######################
    # Data Handling
    def read_csv(
        filename: str, has_header: bool = True, return_dict: bool = True
    ):
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
                raise Exception(
                    "If `return_dict` is True, `has_header` must also be True."
                )
            else:
                return [i for i in file_data]

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
    @pamda_wrappers.curry_wrap
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

    @pamda_wrappers.curry_wrap
    def getForceDict(object: dict, key: str):
        """
        Function:

        - Returns a value from a dictionary given a key and forces that value to be a dictionary
        - Note: This updates the object in place to force the value from the key to be a dictionary

        Requires:

        - `object`:
            - Type: dict
            - What: The object from which to look for a key
        - `key`:
            - Type: str
            - What: The key to look up in the object

        Example:

        ```
        data = {'a':{}, 'b':1}

        pamda.getForceDict(data, 'a') #=> {}
        pamda.getForceDict(data, 'b') #=> {}

        # Note that the object has been updated in place
        data #=> {'a':{}, 'b':{}}
        ```
        """
        if not isinstance(object.get(key), dict):
            object.__setitem__(key, {})
        return object.get(key)
