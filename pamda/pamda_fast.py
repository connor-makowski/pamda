from functools import reduce


def __getForceDict__(object: dict | list, key: str | int | tuple):
    """
    An internal version of pamda_utils.getForceDict designed for calling speed

    """
    if isinstance(object, dict):
        value = object.get(key)
    else:
        value = object[key]
    if not isinstance(value, (dict, list)):
        value = {}
        object.__setitem__(key, value)
    return value


def __assocPath__(path: list | str | int | tuple, value, data: dict):
    """
    An internal version of pamda_utils.assocPath designed for calling speed
    """
    reduce(__getForceDict__, path[:-1], data).__setitem__(path[-1], value)
    return data


def __groupByHashable__(fn, data: list):
    """
    An internal version of pamda.groupBy designed for calling speed

    Function:

    - Splits a list into a dictionary of sublists keyed by the return hashable of a provided function
    - This is a faster version of groupBy without validation overhead
    - It does not require a string return type for the passed fn

    Requires:

    - `fn`:
        - Type: function | method
        - What: The function or method to group by
        - Note: Must return a hashable object
        - Note: This function must be unary (take one input)
        - Note: This function is applied to each item in the list recursively
        - Note: The output of this function is not validated for speed purposes
    - `data`:
        - Type: list
        - What: List of items to apply the function to and then group by the results

    """
    output = {}
    for i in data:
        path = fn(i)
        if path not in output:
            output[path] = []
        output[path].append(i)
    return output


def __mergeDeep__(update_data, data):
    """
    An internal version of pamda.mergeDeep designed for calling speed

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
    if not isinstance(data, dict) or not isinstance(update_data, dict):
        return update_data
    output = dict(data)
    keys_original = set(data.keys())
    keys_update = set(update_data.keys())
    similar_keys = keys_original.intersection(keys_update)
    similar_dict = {
        key: __mergeDeep__(update_data[key], data[key]) for key in similar_keys
    }
    new_keys = keys_update.difference(keys_original)
    new_dict = {key: update_data[key] for key in new_keys}
    output.update(similar_dict)
    output.update(new_dict)
    return output


def __pathOr__(default, path: list, data: dict):
    """
    An internal version of pamda.pathOr designed for calling speed

    Function:

    - Returns the value of a path within a nested dictionary or a default value if that path does not exist
    - Does not accept str as path like pamda.pathOr

    Requires:

    - `default`:
        - Type: any
        - What: The object to return if the path does not exist
    - `path`:
        - Type: list of strs
        - What: The path to pull given the data
    - `data`:
        - Type: dict
        - What: A dictionary to get the path from

    Example:

    ```
    data={'a':{'b':1}}
    pamda.path(default=2, path=['a','c'], data=data) #=> 2
    ```
    """
    return reduce(lambda x, y: x.get(y, {}), path[:-1], data).get(
        path[-1], default
    )


def __getKeyValues__(keys: list, data: dict):
    """
    An internal function to pluck the values of keys out of a dictionary designed for calling speed

    Function:

    - Retrieves the values of a list of keys from a dictionary
    - This is a faster version of getKeys without validation overhead

    Requires:

    - `keys`:
        - Type: list
        - What: The list of keys to retrieve from the dictionary
    - `data`:
        - Type: dict
        - What: The dictionary to retrieve the keys from

    Returns:

    - Type: tuple
    - What: The values of the keys from the dictionary

    """
    return tuple([data[key] for key in keys])
