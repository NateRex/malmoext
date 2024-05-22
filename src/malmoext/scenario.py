import malmo.MalmoPython as MalmoPython
import malmoext.malmo_bootstrap as MalmoBootstrap
from malmo.malmoutils import parse_command_line, get_default_recording_object
from malmoext.scenario_builder import ScenarioBuilder
from abc import abstractmethod
import time

class Scenario:
    '''A Scenario defines the construction of a Minecraft simulation, and the actions that one or more agents should perform
    based on the changing state of that simulation over time.
    
    Each implementation of a Scenario must implement the following two methods:
    - build_scenario - Constructs the starting state of the simulation
    - on_tick - Performs one or more agent actions on each simulation tick'''

    def __init__(self):
        self.__builder = ScenarioBuilder()


    @abstractmethod
    def build_scenario(self, builder: ScenarioBuilder):
        '''Method that constructs the details of a scenario. An empty ScenarioBuilder is provided as input to this method,
        and is expected to be modified prior to returning.

        Example implementation:

            builder.set_description('Swing Sword')

            builder.set_time_limit(30.0)

            builder.add_agent('agent1', AgentType.CPU)

            builder.agents['agent1'].addInventory(Items.All.diamond_sword, Inventory.HotBar._0)

            builder.agents['agent1'].set_position(Vector(0, 4, 0))

            builder.world.addMob(Mobs.Hostile.Zombie, Vector(5, 4, 0))
        '''
        pass


    @abstractmethod
    def on_tick(self):
        '''Method that is called on each clock tick, where any number of agent actions can be initiated. The full
        list of agent actions can be found at https://github.com/NateRex/malmoext/blob/master/docs/agent_actions.md

        The actions performed by an agent may depend on the current game state. Documentation on what state details
        are observable can be found at https://github.com/NateRex/malmoext/blob/master/docs/agent_state.md

        Example implementation:
            
            agent = getAgent()

            mob = agent.closest_mob(Mobs.Hostile)

            if mob != None:
            
                if agent.lookAt(mob) and agent.moveTo(mob):
                
                    agent.attack()

            else:
            
                agent.doNothing()
        '''
        pass
    

    def run(self, ports=[10000]):
        '''Executes this scenario within the Malmo Minecraft instances running on the given ports. By default, a single
        Malmo Minecraft instance running on port 10000 is assumed.
        
        Documentation on how to run one or more Malmo Minecraft instances on different ports can be found at
        https://github.com/NateRex/malmoext/blob/master/README.md#running-a-scenario
        '''

        # Initialize Malmo Platform environment
        MalmoBootstrap.init()

        # Construct scenario
        self.build_scenario(self.__builder)

        # Validate scenario
        numAgents = len(self.__builder.agents)
        if (len(ports) < numAgents):
            raise Exception('Number of agents must not exceed the number of Malmo Minecraft instances currently running.')
        if (numAgents == 0):
            print('No agents present in scenario. Exiting.')
            exit(0)

        # Construct agent client connections
        clientPool = MalmoPython.ClientPool()
        agentHosts = []
        for i in range(0, len(self.__builder.agents)):
            clientPool.add(MalmoPython.ClientInfo('127.0.0.1', ports[i]))
            agentHosts.append(MalmoPython.AgentHost())

        # Load the scenario
        mission = MalmoPython.MissionSpec(self.__builder.build(), True)
        parse_command_line(agentHosts[0])

        # Start the mission
        hostIdx = 0
        for host in agentHosts:
            recordingObject = get_default_recording_object(agentHosts[0], "agent_{}_viewpoint_continuous".format(hostIdx + 1))
            self.__start_host_mission(host, mission, clientPool, recordingObject, hostIdx, '')
            hostIdx += 1
        
        # Wait for mission to start
        self.__wait_for_mission_start(agentHosts)

        # While mission is running, execute agent actions
        while (agentHosts[0].peekWorldState().is_mission_running):
            self.on_tick()
            time.sleep(0.1)


    def __start_host_mission(self, agent_host, mission, client_pool, recording, role, experimentId):
        '''Attempts to start a mission for an agent host. Will automatically retry on failure. After multiple,
        failures, an error will be reported and the program will exit.'''

        used_attempts = 0
        max_attempts = 5
        print("Starting mission for agent ", role)
        while True:
            try:
                agent_host.startMission(mission, client_pool, recording, role, experimentId)
                break
            except MalmoPython.MissionException as e:
                errorCode = e.details.errorCode
                if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                    print("Server not quite ready yet - waiting...")
                    time.sleep(2)
                elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                    print("Not enough available Minecraft instances running.")
                    used_attempts += 1
                    if used_attempts < max_attempts:
                        print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                        time.sleep(2)
                elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                    print("Server not found - has the mission with role 0 been started yet?")
                    used_attempts += 1
                    if used_attempts < max_attempts:
                        print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                        time.sleep(2)
                else:
                    print("Other error:", e.message)
                    print("Waiting will not help here - bailing immediately.")
                    exit(1)
            if used_attempts == max_attempts:
                print("All chances used up - bailing now.")
                exit(1)
        print("startMission called okay.")

    def __wait_for_mission_start(self, agent_hosts):
        '''This method will block execution until all given hosts have succesfully started their mission. If any host
        fails to begin their mission, a timeout error will occur and the program will exit.'''
        print("Waiting for the mission to start", end=' ')
        start_flags = [False for a in agent_hosts]
        start_time = time.time()
        time_out = 120  # Allow two minutes for mission to start.
        while not all(start_flags) and time.time() - start_time < time_out:
            states = [a.peekWorldState() for a in agent_hosts]
            start_flags = [w.has_mission_begun for w in states]
            errors = [e for w in states for e in w.errors]
            if len(errors) > 0:
                print("Errors waiting for mission start:")
                for e in errors:
                    print(e.text)
                print("Bailing now.")
                exit(1)
            time.sleep(0.1)
            print(".", end=' ')
        print()
        if time.time() - start_time >= time_out:
            print("Timed out waiting for mission to begin. Bailing.")
            exit(1)
        print("Mission has started.")