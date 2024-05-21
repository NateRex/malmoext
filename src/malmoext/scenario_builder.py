

class ScenarioBuilder:
    '''A ScenarioBuilder is the top-level builder used to define the agents and objects present in
    each scenario. This information is converted to an XML format that is digestable by the Malmo
    Platform.
    
    An empty ScenarioBuilder instance is provided to the 'init' method of each Scenario, which
    is where construction takes place.'''

    def __init__(self):
        '''Constructor'''
        self.environment = EnvironmentBuilder()

class EnvironmentBuilder:
    '''The EnvironmentBuilder controls environment settings such as mob spawning and structures.
    
    By default, no mobs spawn naturally and the world is completely flat.'''

    def __init__(self):
        '''Constructor'''
        self.__generatorString = '3;7,2*3,2;1;'
        self.__decoratorsXML = ""
        self.__allowedMobs = set([])

    def friendlySpawningOn(self):
        '''Enables the natural spawning of friendly animals and villagers
        '''