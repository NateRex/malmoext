from typing import Any, Union
from malmoext.types import Block, Mob, Item, Inventory, Vector, Rotation, Entity, InventoryItem
from malmoext.utils import Utils
from malmoext.agent import Agent
import json

class AgentState:
    '''An AgentState represents the observable world from the perspective of a single agent.
    It represents an alternative representation of the JSON data provided by Malmo.'''


    def __init__(self, agent: Agent):
        '''Constructor. Accepts the agent whose perspective this state represents.'''
        
        raw_state = agent.get_host().getWorldState()
        raw_data = json.loads(raw_state.observations[-1].text)

        self.__position = self.__parse_position(raw_data)
        self.__pov = self.__parse_pov_camera_angles(raw_data)
        self.__grid = self.__parse_grid(raw_data, agent.get_observable_distances())
        self.__nearby_entities = self.__parse_nearby_entities(raw_data)
        self.__inventory = self.__parse_inventory(raw_data)
        self.__equipped_slot = self.__parse_equipped_slot(raw_data)


    def get_position(self):
        '''Returns the current position of this agent'''
        return self.__position
    

    def get_pov(self):
        '''Returns the current camera angles for this agent's point-of-view (POV)'''
        return self.__pov


    def get_entities(self):
        '''Returns a dictionary containing all entities nearby the agent, organized by type.'''
        return self.__nearby_entities
    
    
    def get_entities(self, mob_type: Mob):
        '''Returns a list containing all nearby entities of the given mob type.'''
        
        if mob_type not in self.__nearby_entities:
            return []
        
        return self.__nearby_entities[mob_type]


    def get_entity_by_type(self, mob_type: Mob):
        '''Returns the closest entity to the agent containing the given type. Returns None if no entity with that
        type exists within the agent's observable range.'''

        if mob_type not in self.__nearby_entities:
            return None
        
        closest_sqrd_distance = None
        closest_entity = None
        for entity in self.__nearby_entities[mob_type]:
            sqrd_distance = Utils.squared_distance(self.__position, entity.position)
            if (closest_entity is None) or (sqrd_distance < closest_sqrd_distance):
                closest_sqrd_distance = sqrd_distance
                closest_entity = entity
        
        return closest_entity


    def get_entity_by_name(self, name: str):
        '''Returns the closest entity to the agent containing the given name. Returns None if no entity with that
        name exists within the agent's observable range.'''

        closest_sqrd_distance = None
        closest_entity = None
        for eType in self.__nearby_entities:
            for entity in self.__nearby_entities[eType]:
                if entity.name == name:
                    sqrd_distance = Utils.squared_distance(self.__position, entity.position)
                    if (closest_entity is None) or (sqrd_distance < closest_sqrd_distance):
                        closest_sqrd_distance = sqrd_distance
                        closest_entity = entity
        
        return closest_entity


    def get_nearby_block(self, rel_pos: Vector):
        '''Returns the type of block present at a location, defined in coordinates relative to the agent.
        
        For example:
        
            get_block(Vector(-1, 0, 0))
        
        would return the type one block away in the negative x direction.
        
        An exception will be thrown if the caller attempts to access a block outside the obserable range
        of the agent.'''

        return self.__grid[rel_pos]


    def get_inventory_item(self, item_type: Item):
        '''Searches the agent inventory for an item of the given type. This method searches the agent's hotbar,
        main inventory, and armor slots, in that order and returns the first instance found. Returns None if the
        agent does not have that item.'''

        if (not item_type in self.__inventory):
            return None
        
        instances = self.__inventory[item_type]
        preferred_instance = None
        for instance in instances:
            if (preferred_instance == None) or (instance.slot.value < preferred_instance.slot.value):
                preferred_instance = instance
        return preferred_instance


    def get_currently_equipped_slot(self):
        '''Returns the inventory hotbar slot currently equipped by the agent.'''

        return self.__equipped_slot


    def get_available_hotbar_slot(self):
        '''Returns the next available hotbar slot for this agent that does not currently contain an item. Returns
        None if all hotbar slots are currently occupied.'''
        
        in_use = set()
        for instances in self.__inventory.values():
            for invItem in instances:
                in_use.add(invItem.slot)
        
        for slot in Inventory.HotBar:
            if slot not in in_use:
                return slot
            
        return None


    def __parse_position(self, raw_data):
        '''Parses a raw observation object to determine the current position of the agent.'''
        
        return Vector(raw_data['XPos'], raw_data['YPos'], raw_data['ZPos'])
    

    def __parse_pov_camera_angles(self, raw_data):
        '''Parses a raw observation object to determine the current camera angles of the agent'''

        # Ensure we normalize yaw to the range (0, 360)
        yaw = raw_data['Yaw']
        yaw = (yaw + 360) % 360
        
        return Rotation(yaw, raw_data['Pitch'])


    def __parse_nearby_entities(self, raw_data):
        '''Parses a raw observation object to determine all entities near the agent. An entity is defined as a mob,
        a drop item, or another agent.
        
        Returns a dictionary containing all nearby entities to the agent, organized by type.'''
        
        entities = {}     # type: dict[Union[Mob, Item], list[Entity]]
        for obj in raw_data['nearby_entities']:

            if Item.contains(obj['name']):
                eType = Item(obj['name'])
            elif Mob.contains(obj['name']):
                eType = Mob(obj['name'])
            else:
                # Assume entity is agent
                eType = Mob.agent

            ePos = Vector(obj['x'], obj['y'], obj['z'])
            entity = Entity(obj['id'], eType, obj['name'], ePos, obj.get('quantity', 1))
            Utils.add_or_append(entities, eType, entity)
        
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
        grid = {}      # type: dict[Vector, Block]
        for x in range(-observable_distances.x, observable_distances.x):
            for z in range(-observable_distances.z, observable_distances.z):
                for y in range(-observable_distances.y, observable_distances.y):
                    grid[Vector(x, y, z)] = Block(raw_grid[idx])
                    idx += 1
        return grid
    

    def __parse_inventory(self, raw_data: Any):
        '''Parses a raw observation object to determine the current inventory of an agent.
        
        The resulting dictionary contains all items in the agent's inventory, organized by type.'''

        raw_inventory = raw_data['inventory']

        inventory = {}     # type: dict[Item, list[InventoryItem]]
        for obj in raw_inventory:
            iType = Item(obj['type'])
            index = obj['index']

            # Determine inventory slot
            if Inventory.HotBar.contains(index):
                slot = Inventory.HotBar(index)
            elif Inventory.Main.contains(index):
                slot = Inventory.Main(index)
            elif Inventory.Armor.contains(index):
                slot = Inventory.Armor(index)

            inventoryItem = InventoryItem(iType, obj['quantity'], slot)
            Utils.add_or_append(inventory, iType, inventoryItem)

        return inventory


    def __parse_equipped_slot(self, raw_data: Any):
        '''Parses a raw observation object to determine the currently equipped inventory slot of the agent.'''

        return raw_data['currentItemIndex']