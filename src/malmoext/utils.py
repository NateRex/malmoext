from typing import Any
from malmoext.types import Vector
import math

def add_or_append(dictionary: "dict[Any, list[Any]]", key: Any, value: Any):
    '''For a dictionary whose values are lists, this method will attempt to append a value to the list associated
    with a key, if it already exists. Otherwise, a new entry will be added.'''
    
    if (key in dictionary):
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

def squared_distance(p1: Vector, p2: Vector):
    '''Returns the squared distance between two points.'''
    return math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2) + math.pow(p2.z - p1.z, 2)