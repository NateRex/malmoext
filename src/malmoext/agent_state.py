from typing import Any
from malmoext.types import Vector, Block

class AgentState:
    '''An AgentState represents the observable world from the perspective of a single agent.
    It represents an alternative representation of the JSON data provided by Malmo.'''

    def __init__(self, raw_data: Any, observable_distances: Vector):
        '''Constructor. Accepts the raw observation object returned from Malmo Minecraft representing
        the state for an agent, as well as the dimensions in which to divide the observation grid.'''
        self.__grid = self.__parse_grid(raw_data, observable_distances)
        self.__nearbyEntities = self.__parse_nearby_entities(raw_data)

    def get_block(self, rel_pos: Vector):
        '''Returns the type of block present at a location, defined in coordinates relative to the agent.
        
        For example, get_block(Vector(-1, 0, 0)) would return the type one block away in the negative
        x direction'''

        return self.__grid[rel_pos]

    def __parse_nearby_entities(self):
        '''Returns a map containing all nearby entities'''

    def __parse_grid(self, raw_data: Any, observable_distances: Vector):
        '''Parses a raw observation object to determine the 3-dimensional grid of blocks surrounding the
        agent. The resulting grid is indexed using block locations relative to the agent.'''
        
        expected_size = (observable_distances.x * 2 + 1) * (observable_distances.y * 2 + 1) * (observable_distances.z * 2 + 1)
        actual_size = len(raw_data.blockgrid)
        if (expected_size != actual_size):
            raise Exception('Block grid received from server did not match expected observation size')

        idx = 0
        grid: dict[Vector, Block] = {}
        for x in range(-observable_distances.x, observable_distances.x):
            for z in range(-observable_distances.z, observable_distances.z):
                for y in range(-observable_distances.y, observable_distances.y):
                    grid[Vector(x, y, z)] = Block(raw_data.blockgrid[idx])
                    idx += 1
        return grid
