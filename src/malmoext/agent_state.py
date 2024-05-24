from typing import Any, Union
from malmoext.types import Block, Mob, Item, Inventory, Vector, Entity, InventoryItem
from malmoext.utils import add_or_append
from malmoext.agent import Agent
import json

class AgentState:
    '''An AgentState represents the observable world from the perspective of a single agent.
    It represents an alternative representation of the JSON data provided by Malmo.'''


    def __init__(self, agent: Agent):
        '''Constructor. Accepts the agent whose perspective this state represents.'''
        
        raw_state = agent.get_host().getWorldState()
        raw_data = json.loads(raw_state.observations[-1].text)

        self.__grid = self.__parse_grid(raw_data, agent.get_observable_distances())
        self.__nearby_entities = self.__parse_nearby_entities(raw_data)
        self.__inventory = self.__parse_inventory(raw_data)
        self.__equipped_slot = self.__parse_equipped_slot(raw_data)

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
                # Assume entity is agent
                eType = Mob.agent

            ePos = Vector(obj['x'], obj['y'], obj['z'])
            entity = Entity(obj['id'], eType, obj['name'], ePos, obj.get('quantity', 1))
            add_or_append(entities, eType, entity)
        
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
    

    def __parse_inventory(self, raw_data: Any):
        '''Parses a raw observation object to determine the current inventory of an agent.
        
        The resulting dictionary contains all items in the agent's inventory, organized by type.'''

        raw_inventory = raw_data['inventory']

        inventory: dict[Item, list[InventoryItem]] = {}
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
            add_or_append(inventory, iType, inventoryItem)

        return inventory


    def __parse_equipped_slot(self, raw_data: Any):
        '''Parses a raw observation object to determine the currently equipped inventory slot of the agent.'''

        return raw_data['currentItemIndex']