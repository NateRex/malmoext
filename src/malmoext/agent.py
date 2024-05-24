import malmo.MalmoPython as MalmoPython
from malmoext.scenario_builder import AgentBuilder
from malmoext.types import Item, Inventory

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

        

# Additional imports to avoid circular dependencies
from malmoext.agent_state import AgentState