from typing import Union
from malmoext.types import Mob, Block, Item, Direction, Inventory, TimeOfDay, AgentType, Vector

class ScenarioBuilder:
    '''A ScenarioBuilder is the top-level builder used to define the agents and objects present in
    each scenario. This information is converted to an XML format that is digestable by the Malmo
    Platform.
    
    An empty ScenarioBuilder instance is provided to the 'init' method of each Scenario, which
    is where construction takes place.'''

    def __init__(self):
        '''Constructor'''

        self.__description = ''
        self.__timeLimit = 3600.0
        self.__timeOfDay = TimeOfDay.Noon
        self.world = WorldBuilder()
        self.agents: dict[str, AgentBuilder] = {}

    def set_description(self, description):
        '''Set a description for this scenario.'''

        self.__description = description
        return self

    def set_time_limit(self, timeLimit: float):
        '''Set the time limit for the scenario (in decimal seconds).'''
        
        self.__timeLimit = timeLimit
        return self

    def set_time_of_day(self, timeOfDay: Union[int, TimeOfDay]):
        '''Set the Minecraft time of day to a static value'''

        if type(timeOfDay) == int:
            self.__timeOfDay = timeOfDay
        else:
            self.__timeOfDay = timeOfDay.value
        return self

    def add_agent(self, name, type):
        '''Adds a new agent to the scenario. The builder for this new agent can later be accessed via
        the 'agents' dictionary stored on the ScenarioBuilder.'''

        if (name in self.agents):
            raise Exception('Two agents cannot have the same name: ' + name)

        self.agents[name] = AgentBuilder(name, type)
        return self
    
    def build(self):
        '''Builds an XML string representing the contents of this builder that can be read by the Malmo Platform'''
        
        # Convert time limit to ms
        timeLimitMs = int(self.__timeLimit * 1000)

        # Convert mob spawn list to a string
        mobSpawnList = self.world.get_mobs_allowed_to_spawn()
        mobSpawnStr = ""
        for mob in mobSpawnList:
            mobSpawnStr = mobSpawnStr + mob + " "

        # Build xml data for world data
        xml = '''
        <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>{}</Summary>
            </About>

            <ServerSection>
                    <ServerInitialConditions>
                        <Time>
                            <StartTime>{}</StartTime>
                            <AllowPassageOfTime>false</AllowPassageOfTime>
                        </Time>
                        <Weather>clear</Weather>
                        <AllowSpawning>{}</AllowSpawning>
                        <AllowedMobs>{}</AllowedMobs>
                    </ServerInitialConditions>
            
                <ServerHandlers>
                        {}
                        <ServerQuitFromTimeUp timeLimitMs="{}" description="out_of_time"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>
            '''.format(self.__description, self.__timeOfDay, "false" if len(mobSpawnList) == 0 else "true", mobSpawnStr, self.world.build(), timeLimitMs)
        
        # Add XML for each agent
        for agent in self.agents.values():
            xml += agent.build()

        return xml + "</Mission>"

class WorldBuilder:
    '''The WorldBuilder enables the placement of structures, mobs, and items within the Minecraft
    world. It also allows the user to toggle on/off the natural spawning of different mob types.
    
    By default, natural mob spawning is disabled for all types of mobs.'''

    def __init__(self):
        '''Constructor'''
        
        self.__generatorString = '3;7,2*3,2;1;'
        self.__decoratorsXML = ""
        self.__allowedToSpawn: set[list[str]] = set([])

    def get_mobs_allowed_to_spawn(self):
        '''Returns the set of mob names that are allowed to naturally spawn'''
        return self.__allowedToSpawn

    def friendly_spawning_on(self):
        '''Enables the natural spawning of friendly animals and villagers'''

        for m in Mob.Peaceful:
            self.__allowedToSpawn.add(m.value)
        return self

    def friendly_spawning_off(self):
        '''Disables the natural spawning of friendly animals and villagers'''

        for m in Mob.Peaceful:
            self.__allowedToSpawn.discard(m.value)
        return self

    def monster_spawning_on(self):
        '''Enables the natural spawning of hostile enemies'''

        for m in Mob.Hostile:
            self.__allowedToSpawn.add(m.value)
        return self

    def monster_spawning_off(self):
        '''Disables the natural spawning of hostile enemies'''

        for m in Mob.Hostile:
            self.__allowedToSpawn.discard(m.value)
        return self

    def add_block(self, block: Block, p: Vector, variant: Mob.All = None):
        '''Adds a single block to the world. If the block type is a mob spawner, an additional variant value must
        be provided describing the type of mob.'''

        if (variant != None):
            self.__decoratorsXML += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" variant="{}"/>'''.format(p.x, p.y, p.z, block.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawBlock x="{}" y="{}" z="{}" type="{}"/>'''.format(p.x, p.y, p.z, block.value)
        return self

    def add_cube(self, block: Block, p1: Vector, p2: Vector,
            variant: Mob.All = None):
        '''Adds a cuboid consisting of single block type to the world. The cube is formed from two points
        on opposite corners of the cube. If the block type is a mob spawner, an additional variant value must
        be provided describing the type of mob.'''

        if (variant != None):
            self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}" variant="{}"/>'''.format(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z, block.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z, block.value)
        return self

    def add_line(self, block: Block, p1: Vector, p2: Vector,
            variant: Mob.All = None):
        '''Adds a line consisting of a single block type to the world. The line is formed from the given
        two points. If the block type is a mob spawner, an additional variant value must be provided describing
        the type of mob.'''

        if (variant != None):
            self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}" variant="{}"/>'''.format(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z, block.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z, block.value)
        return self

    def add_sphere(self, block, center, radius, variant = None):
        '''Add a sphere consisting of a single block type to the world. The sphere is formed from a center point and radius.
        If the block type specified is a mob spawner, an additional variant value must be provided describing the type of
        mob.'''

        if (variant != None):
            self.__decoratorsXML += '''<DrawSphere x="{}" y="{}" z="{}" radius="{}" type="{}" variant="{}"/>'''.format(center.x, center.y, center.z, radius, block.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawSphere x="{}" y="{}" z="{}" radius="{}" type="{}"/>'''.format(center.x, center.y, center.z, radius, block.value)
        return self

    def add_item(self, item: Item, p: Vector):
        '''Adds a drop-item to the world at a specific coordinate location.'''

        self.__decoratorsXML += '''<DrawItem x="{}" y="{}" z="{}" type="{}"/>'''.format(p.x, p.y, p.z, item.value)
        return self

    def add_mob(self, mob: Mob, p: Vector):
        '''Positions a mob at a specific coordinate location.'''

        self.__decoratorsXML += '''<DrawEntity x="{}" y="{}" z="{}" type="{}"/>'''.format(p.x, p.y, p.z, mob.value)
        return self

    def build(self):
        '''Builds an XML string representing the contents of this builder that can be read by the Malmo Platform'''

        return '''
        <FlatWorldGenerator forceReset="true" generatorString="{}"/>
        {}
        '''.format(self.__generatorString, "<DrawingDecorator>" + self.__decoratorsXML + "</DrawingDecorator>" if len(self.__decoratorsXML) > 0 else "")


class AgentBuilder:
    '''The AgentBuilder enables the creation of human or CPU-controlled agents within the Minecraft world.'''
    
    def __init__(self, name: str, type: AgentType):
        '''Constructor. Accepts a name for the new agent being constructed.'''

        self.__name = name
        self.__type = type
        self.__pos = Vector(0., 0., 0.)
        self.__dir = Direction.North.value
        self.__observableDistances = Vector(10, 5, 10)
        self.__inventoryXML = ''
        self.__handlersXML = ''

    def get_name(self):
        '''Return the name of this agent'''
        return self.__name
    
    def get_type(self):
        '''Return this agent's type'''
        return self.__type
    
    def get_observable_distances(self):
        '''Returns the observable distance of this agent in the x, y, and z directions'''
        return self.__observableDistances

    def set_position(self, pos):
        '''Set the starting location for this agent'''
        self.__pos = pos
        return self

    def set_direction(self, dir: Union[int, Direction]):
        '''Set the direction that this agent should start out facing'''
        if type(dir) == int:
            self.__dir = dir
        else:
            self.__dir = dir.value
        return self

    def set_observable_distances(self, values: Vector):
        '''Sets the observable distance of this agent in the x, y, and z directions'''
        self.__observableDistances = values

    def add_inventory_item(self, item: Item, slot: Inventory, quantity: int = 1):
        '''Adds an item to the agent's inventory in a given slot. If the item is stackable, a quantity may be specified.'''
        self.__inventoryXML += '''<InventoryItem slot="{}" type="{}" quantity="{}"/>'''.format(slot.value, item.value, quantity)
        return self

    def build(self):
        '''Builds an XML string representing the contents of this builder that can be read by the Malmo Platform'''

        return '''
        <AgentSection mode="Survival">
        <Name>{}</Name>
        <AgentStart>
            <Placement x="{}" y="{}" z="{}" yaw="{}"/>
            <Inventory>
            {}
            </Inventory>
        </AgentStart>
        <AgentHandlers>
        <ObservationFromFullStats/>
        <ObservationFromFullInventory flat="false"/>
        <InventoryCommands/>
        <SimpleCraftCommands/>
        <MissionQuitCommands/>
        <ContinuousMovementCommands/>
        <ObservationFromGrid>
            <Grid name="blockgrid">
                <min x="{}" y="{}" z="{}"/>
                <max x="{}" y="{}" z="{}"/>
            </Grid>
        </ObservationFromGrid>
        <ObservationFromNearbyEntities>
            <Range name="nearby_entities" xrange="25" yrange="2" zrange="25" />
        </ObservationFromNearbyEntities>
        {}
        </AgentHandlers>
        </AgentSection>'''.format(self.__name, self.__pos.x, self.__pos.y, self.__pos.z, self.__dir, self.__inventoryXML, -self.__observableDistances.x, -self.__observableDistances.y, -self.__observableDistances.z, self.__observableDistances.x, self.__observableDistances.y, self.__observableDistances.z, self.__handlersXML)