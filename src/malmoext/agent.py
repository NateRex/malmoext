import malmo.MalmoPython as MalmoPython
from typing import Union
from malmoext.scenario_builder import AgentBuilder
from malmoext.types import Item, Inventory, Entity, Vector, Rotation
from malmoext.utils import vector_to, normalize, is_zero_vector, linear_map, equal_tol, TWO_PI
import math

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


    def equip(self, item_type: Item) -> bool:
        '''Equips an item from this agent's inventory. If the item does not already exist in the agent's hotbar,
        it will be swapped with an item from the hotbar. Returns true if successful. Returns false otherwise.'''
        
        inventory_item = self.state.get_inventory_item(item_type)
        if inventory_item is None:
            return False
        
        # Malmo keys are 1-indexed
        item_index = inventory_item.slot.value
        target_index = item_index

        # If item is not already in the hotbar...
        if not Inventory.HotBar.contains(item_index):
            
            # Try to move item into an empty hotbar slot. Otherwise, swap item with what is currently equipped
            target_slot = self.state.get_available_hotbar_slot()
            if target_slot is None:
                target_slot = self.state.get_currently_equipped_slot()
            target_index = target_slot.value
            self.__host.sendCommand('swapInventoryItems {} {}'.format(target_index, item_index))

        # Equip (Malmo keys are 1-indexed)
        self.__host.sendCommand('hotbar.{} 1'.format(target_index + 1))
        self.__host.sendCommand('hotbar.{} 0'.format(target_index + 1))
        return True


    def look_at(self, entity: Union[str, Entity]):
        '''Initiates camera movement of this agent's POV to face another entity, specified either by name or by reference.
        If multiple entities contain the given name, the closest one will be targeted.
        
        Because this transition does not occur instantaneously, this method is intended to be called repeatedly as part
        of the simulation loop.
        
        Returns true if the agent is currently facing the entity (and thus no further camera change will occur). Returns
        false if the agent is not yet facing the entity, or an entity with the given name does not exist.'''

        target = entity
        if isinstance(target, str):
            target = self.state.get_entity_by_name(target)
        
        if target is None:
            return False
        
        turn_rates = self.__compute_turn_rates(target.position)

        # Modify yaw rate
        if equal_tol(turn_rates.yaw, 0, 0.001):
            self.__host.sendCommand('turn 0')
        else:
            self.__host.sendCommand('turn {}'.format(turn_rates.yaw))
    
        # Modify pitch rate
        if equal_tol(turn_rates.pitch, 0, 0.001):
            self.__host.sendCommand('pitch 0')
        else:
            self.__host.sendCommand('pitch {}'.format(turn_rates.pitch))
        
    
    def __compute_turn_rates(self, target_position: Vector):
        '''Calculates proposed yaw and pitch angle rotations for the camera, in order to face the given position.'''

        # Get vector from agent to target
        agent_position = self.state.get_position()
        agent_pov = self.state.get_pov()
        v = vector_to(agent_position, target_position)
        v = normalize(v)
        if is_zero_vector(v, 1.0e-6):
            return Rotation(0, 0)

        # Target pitch (-90, 90)
        target_pitch = math.atan(-v.y / math.sqrt(v.z * v.z + v.x * v.x))
        target_pitch = math.degrees(target_pitch)

        # Target yaw (0, 360)
        target_yaw = math.atan2(-v.x, v.z)
        target_yaw = math.degrees((target_yaw + TWO_PI) % TWO_PI)

        # Pitch turning direction
        pitch_turn_direction = 1 if target_pitch > agent_pov.pitch else -1
        pitch_diff = abs(target_pitch - agent_pov.pitch)

        # Yaw turning direction. We want to rotate in whatever direction results in the least amount of turning.
        yaw_diff = abs(agent_pov.yaw - target_yaw)
        yaw_turn_direction = 1 if target_yaw > agent_pov.yaw else -1
        yaw_diff_2 = 360 - yaw_diff
        if yaw_diff_2 < yaw_diff:
            yaw_diff = yaw_diff_2
            yaw_turn_direction = -yaw_turn_direction

        # Rotation speeds
        yaw_rate = min(linear_map(yaw_diff, 0, 180, 0, 2), 1) * yaw_turn_direction
        pitch_rate = min(linear_map(pitch_diff, 0, 180, 0, 2), 1) * pitch_turn_direction
        return Rotation(yaw_rate, pitch_rate)


# Additional imports to avoid circular dependencies
from malmoext.agent_state import AgentState