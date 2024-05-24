from typing import Any

def add_or_append(dictionary: "dict[Any, list[Any]]", key: Any, value: Any):
    '''For a dictionary whose values are lists, this method will attempt to append a value to the list associated
    with a key, if it already exists. Otherwise, a new entry will be added.'''
    
    if (key in dictionary):
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]