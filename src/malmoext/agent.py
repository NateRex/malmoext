from typing import Any, Union
import malmo.MalmoPython as MalmoPython
from malmoext.scenario_builder import AgentBuilder
from malmoext.types import Vector, Block, Mob, Item, Entity
import json

class Agent:
    '''An Agent wraps a client connection to a Malmo Minecraft instance, and represents a
    player agent in a scenario. The various methods of this class represent the different
    agent actions that can be performed.
    
    Instances of this class should not be constructed directly. Instead, they will be
    automatically constructed when a scenario is ran.'''


    def __init__(self, builder: AgentBuilder):
        '''Constructor'''
        self.__name = builder.get_name()
        self.__observable_distances = builder.get_observable_distances()
        self.__host = MalmoPython.AgentHost()
        self.state: AgentState = None


    def get_name(self):
        '''Returns the name of this agent'''
        return self.__name
    

    def get_observable_distances(self):
        '''Returns the observable distance of this agent in the x, y, and z directions'''
        return self.__observable_distances


    def get_host(self):
        '''Returns a reference to the Malmo AgentHost connection to the Minecraft server'''
        return self.__host
    

    def is_mission_active(self) -> bool:
        '''Returns true if this agent's mission is still active. Returns false otherwise.'''
        return self.__host.peekWorldState().is_mission_running
    

    def sync(self):
        '''Syncs the data cached on this agent with the latest available data from the Malmo Minecraft server'''
        self.state = AgentState(self)
        

class AgentState:
    '''An AgentState represents the observable world from the perspective of a single agent.
    It represents an alternative representation of the JSON data provided by Malmo.'''


    def __init__(self, agent: Agent):
        '''Constructor. Accepts the agent whose perspective this state represents.'''
        
        raw_state = agent.get_host().getWorldState()
        raw_data = json.loads(raw_state.observations[-1].text)

        self.__grid = self.__parse_grid(raw_data, agent.get_observable_distances())
        self.__nearby_entities = self.__parse_nearby_entities(raw_data)


    def get_nearby_entities(self):
        '''Returns a dictionary containing all entities nearby the agent, organized by type.'''
        return self.__nearby_entities


    def get_nearby_block(self, rel_pos: Vector):
        '''Returns the type of block present at a location, defined in coordinates relative to the agent.
        
        For example:
        
            get_block(Vector(-1, 0, 0))
        
        would return the type one block away in the negative x direction.
        
        An exception will be thrown if the caller attempts to access a block outside the obserable range
        of the agent.'''

        return self.__grid[rel_pos]


    def __parse_nearby_entities(self, raw_data):
        '''Parses a raw observation object to determine all entities near the agent. An entity is defined as a mob,
        a drop item, or another agent.
        
        Returns a dictionary containing all nearby entities to the agent, organized by type.'''
        
        entities: dict[Union[Mob, Item], list[Entity]] = {}
        for obj in raw_data['nearby_entities']:

            if Item.contains(obj['name']):
                eType = Item(obj['name'])
            elif Mob.contains(obj['name']):
                eType = Mob(obj['name'])
            else:
                eType = Mob.agent

            ePos = Vector(obj['x'], obj['y'], obj['z'])
            entity = Entity(obj['id'], eType, obj['name'], ePos, obj.get('quantity', 1))
            
            if (eType in entities):
                entities[eType].append(entity)
            else:
                entities[eType] = [entity]
        
        return entities


    def __parse_grid(self, raw_data: Any, observable_distances: Vector):
        '''Parses a raw observation object to determine the 3-dimensional grid of blocks surrounding the
        agent. The resulting grid is indexed using block locations relative to the agent.'''
        
        raw_grid = raw_data['blockgrid']

        expected_size = (observable_distances.x * 2 + 1) * (observable_distances.y * 2 + 1) * (observable_distances.z * 2 + 1)
        actual_size = len(raw_grid)
        if (expected_size != actual_size):
            raise Exception('Block grid received from server did not match expected observation size')

        idx = 0
        grid: dict[Vector, Block] = {}
        for x in range(-observable_distances.x, observable_distances.x):
            for z in range(-observable_distances.z, observable_distances.z):
                for y in range(-observable_distances.y, observable_distances.y):
                    grid[Vector(x, y, z)] = Block(raw_grid[idx])
                    idx += 1
        return grid
