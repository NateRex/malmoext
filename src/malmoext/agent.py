import malmo.MalmoPython as MalmoPython
from malmoext.scenario_builder import AgentBuilder
from malmoext.agent_state import AgentState
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
        self.__type = builder.get_type()
        self.__observableDistances = builder.get_observable_distances()
        self.__host = MalmoPython.AgentHost()
        self.state: AgentState = None

    def is_mission_active(self) -> bool:
        '''Returns true if this agent's mission is still active. Returns false otherwise.'''
        return self.__host.peekWorldState().is_mission_running

    def get_name(self):
        '''Returns the name of this agent'''
        return self.__name
    
    def get_type(self):
        '''Returns this agent's type'''
        return self.__type

    def get_host(self):
        '''Returns a reference to the Malmo AgentHost connection to the Minecraft server'''
        return self.__host
    
    def sync(self):
        '''Updates all cached data on this agent with the latest available data from the Malmo Minecraft server'''
        json_str = self.__host.getWorldState()
        json_obj = json.loads(json_str.observations[-1].text)
        self.state = AgentState(json_obj, self.__observableDistances)