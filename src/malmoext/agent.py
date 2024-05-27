import malmo.MalmoPython as MalmoPython
from typing import Union
from malmoext.scenario_builder import AgentBuilder
from malmoext.types import Item, Inventory, Entity, Vector, Rotation
from malmoext.utils import Utils
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
        self.state = None   # type: AgentState


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
        '''Syncs the data cached on this agent with the latest available data from the Malmo Minecraft server. Returns
        true if new data has been loaded. Returns false otherwise.
        
        This method does not need to be called explicitly by users of this library, as it is called automatically during
        simulation of a scenario.'''

        if self.__host.peekWorldState().number_of_observations_since_last_state > 0:
            self.state = AgentState(self)
            return True

        return False


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
        If multiple entities exist with the given name, the closest one will be targeted.
        
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
        is_looking_at = True

        # Modify yaw rate
        if Utils.equal_tol(turn_rates.yaw, 0, 0.001):
            self.__host.sendCommand('turn 0')
        else:
            self.__host.sendCommand('turn {}'.format(turn_rates.yaw))
            is_looking_at = False
    
        # Modify pitch rate
        if Utils.equal_tol(turn_rates.pitch, 0, 0.001):
            self.__host.sendCommand('pitch 0')
        else:
            self.__host.sendCommand('pitch {}'.format(turn_rates.pitch))
            is_looking_at = False

        return is_looking_at
    

    def move_to(self, entity: Union[str, Entity], keep_distance = 2):
        '''Initiates movement of this agent to another entity, specified either by name or by reference. If multiple
        entities exist with the given name, the closest one will be targeted. Optionally specify a number of blocks the
        agent should keep away from the target (defaults to 2, since two entities cannot occupy the same block). This
        can be useful in cases where the agent plans to attack or give an item to the target.
        
        Because this transition does not occur instantaneously, this method is inteded to be called repeatedly as part
        of the simulation loop.
        
        Returns true if the agent is currently at the entity (with a tolerance of 2 blocks, given that two entities cannot
        always occupy the same block). Returns false otherwise.'''

        target = entity
        if isinstance(target, str):
            target = self.state.get_entity_by_name(target)
        if target is None:
            return False
        
        move_rates = self.__compute_move_rates(target.position, keep_distance)
        is_at = True

        # Modify left/right movement rate
        if Utils.equal_tol(move_rates.x, 0, 0.001):
            self.__host.sendCommand('strafe 0')
        else:
            self.__host.sendCommand('strafe {}'.format(move_rates.x))
            is_at = False

        # Modify forward/backward movement rate
        if Utils.equal_tol(move_rates.z, 0, 0.001):
            self.__host.sendCommand('move 0')
        else:
            self.__host.sendCommand('move {}'.format(move_rates.z))
            is_at = False

        return is_at
        
    
    def __compute_turn_rates(self, target_position: Vector):
        '''Calculates proposed yaw and pitch angle rotations for the camera, in order to face the given position.'''

        # Compute signed angle differences
        angle_diffs = self.__compute_angle_diffs(target_position)
        yaw_turn_direction = 1 if angle_diffs.yaw >= 0 else -1
        pitch_turn_direction = 1 if angle_diffs.pitch >= 0 else -1

        # Compute rotation speeds
        yaw_rate = min(Utils.linear_map(abs(angle_diffs.yaw), 0, 180, 0, 2.25), 1) * yaw_turn_direction
        pitch_rate = min(Utils.linear_map(abs(angle_diffs.pitch), 0, 180, 0, 2.25), 1) * pitch_turn_direction

        return Rotation(yaw_rate, pitch_rate)


    def __compute_move_rates(self, target_position: Vector, tolerance = 2):
        '''Calculates proposed strafing (left/right) and movement (forward/backward) speeds in order to move
        to the given position. Optionally specify a tolerance in number of blocks (defaults to 2, since two entities
        cannot occupy the same block).
        
        Returns the result as a vector, where the x component represents the strafing rate, and the z component
        represents the movement rate.'''

        # If we are already at the target position, return the zero vector for the rates
        target_distance = Utils.distance(self.state.get_position(), target_position)
        if Utils.equal_tol(target_distance, 0, tolerance):
            return Vector(0, 0, 0)

        # Compute signed angle differences and use that to determine side-to-side and forward-backward movement
        angle_diffs = self.__compute_angle_diffs(target_position)
        strafe_rate = math.sin(math.radians(angle_diffs.yaw))
        move_rate = math.cos(math.radians(angle_diffs.yaw))
        return Vector(strafe_rate, 0, move_rate)


    def __compute_angle_diffs(self, target_position: Vector):
        '''Computes the signed angle differences between the agent's line-of-sight and a target position (in degrees).
        
        Returns the resulting two angles, where yaw will be in the range (-180, 180), and pitch will be in the range (-90, 90).'''
       
        # Get vector from agent to target
        agent_position = self.state.get_position()
        v = Utils.vector_to(agent_position, target_position)
        v = Utils.normalize(v)
        if Utils.is_zero_vector(v, 1.0e-6):
            return Rotation(0, 0)

        # Target pitch (-90, 90)
        target_pitch = math.atan(-v.y / math.sqrt(v.z * v.z + v.x * v.x))
        target_pitch = math.degrees(target_pitch)

        # Target yaw (0, 360)
        target_yaw = math.atan2(-v.x, v.z)
        target_yaw = math.degrees((target_yaw + Utils.TWO_PI) % Utils.TWO_PI)

        # Get agent and target angles
        agent_pov = self.state.get_pov()

        # Pitch turning direction
        pitch_diff = abs(target_pitch - agent_pov.pitch)
        pitch_diff *= (1 if target_pitch > agent_pov.pitch else -1)

        # Yaw turning direction. We want to rotate in whatever direction results in the least amount of turning.
        yaw_diff = abs(agent_pov.yaw - target_yaw)
        yaw_turn_direction = 1 if target_yaw > agent_pov.yaw else -1
        yaw_diff_2 = 360 - yaw_diff
        if yaw_diff_2 < yaw_diff:
            yaw_diff = yaw_diff_2
            yaw_turn_direction = -yaw_turn_direction
        yaw_diff = yaw_diff * yaw_turn_direction

        return Rotation(yaw_diff, pitch_diff)



# Additional imports to avoid circular dependencies
from malmoext.agent_state import AgentState