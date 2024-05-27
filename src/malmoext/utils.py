from typing import Any
from malmoext.types import Vector
import math

class Utils:
    '''Class containing purely static utility methods used throughout this library.'''

    PI_OVER_TWO = math.pi / 2
    '''Value of PI divided by two'''

    TWO_PI = math.pi * 2
    '''Value of PI times two.'''

    @staticmethod
    def add_or_append(dictionary: "dict[Any, list[Any]]", key: Any, value: Any):
        '''For a dictionary whose values are lists, this method will attempt to append a value to the list associated
        with a key, if it already exists. Otherwise, a new entry will be added.'''
        
        if (key in dictionary):
            dictionary[key].append(value)
        else:
            dictionary[key] = [value]

    @staticmethod
    def equal_tol(value1: float, value2: float, tol: float):
        '''Returns true if the two values are equal, within tolerance. Returns false otherwise.'''
        abs_diff = abs(value1 - value2)
        return abs_diff <= tol

    @staticmethod
    def linear_map(value, x1, x2, a1, a2):
        '''Linearly maps a value from the range [x1, x2] to the range [a1, a2].'''
        return (value - x1) * (a2 - a1) / (x2 - x1) + a1

    @staticmethod
    def squared_distance(p1: Vector, p2: Vector):
        '''Returns the squared distance between two points.'''
        return math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2) + math.pow(p2.z - p1.z, 2)

    @staticmethod
    def distance(p1: Vector, p2: Vector):
        '''Returns the distance between two points.'''
        return math.sqrt(Utils.squared_distance(p1, p2))

    @staticmethod
    def magnitude(v: Vector):
        '''Computes the magnitude of a vector'''
        return math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)

    @staticmethod
    def normalize(v: Vector):
        '''Normalizes a vector, returning the result as a new vector. Returns the zero vector if the given
        vector has magnitude zero'''
        mag = Utils.magnitude(v)
        if Utils.equal_tol(mag, 0, 1.0e-14):
            return Vector(0, 0, 0)
        else:
            return Vector(v.x / mag, v.y / mag, v.z / mag)
        
    @staticmethod
    def vector_to(p1: Vector, p2: Vector):
        '''Returns the vector from p1 to p2.'''
        return Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

    @staticmethod
    def is_zero_vector(v: Vector, tol = 0.0):
        '''Returns true if the given vector is the zero vector. An optional tolerance can be specified (defaults to 0).'''
        return Utils.equal_tol(v.x, 0, tol) and Utils.equal_tol(v.y, 0, tol) and Utils.equal_tol(v.z, 0, tol)
