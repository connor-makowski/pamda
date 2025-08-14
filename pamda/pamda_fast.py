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
    reduce(__getForceDict__, path[:-1], data).__setitem__(
        path[-1], value
    )
    return data

def __groupByHashable__(fn, data: list):
    """
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
        path_item = output.get(path, [])
        if not path_item:
            output[path] = path_item
        path_item.append(i)
    return output