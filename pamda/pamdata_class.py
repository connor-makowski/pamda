import json, csv
from pamda.pamda_utils import pamda_utils

class pamdata_class(pamda_utils):
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
