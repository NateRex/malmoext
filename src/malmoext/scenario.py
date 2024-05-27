import malmo.MalmoPython as MalmoPython
from malmoext.malmo_bootstrap import MalmoBootstrap
from malmo.malmoutils import parse_command_line, get_default_recording_object
from malmoext.scenario_builder import ScenarioBuilder
from malmoext.agent import Agent
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
        self.__agents = {}    # type: dict[str, Agent]


    @abstractmethod
    def build_scenario(self, builder: ScenarioBuilder) -> None:
        '''Method that constructs the details of a scenario. An empty ScenarioBuilder is provided as input to this method,
        and is expected to be modified prior to returning.

        Example implementation:

            builder.set_description('Swing Sword')

            builder.set_time_limit(30.0)

            builder.add_agent('agent1')

            builder.agents['agent1'].addInventory(Items.All.diamond_sword, Inventory.HotBar._0)

            builder.agents['agent1'].set_position(Vector(0, 4, 0))

            builder.world.addMob(Mobs.Zombie, Vector(5, 4, 0))
        '''
        pass


    @abstractmethod
    def on_tick(self, agents: 'dict[str, Agent]') -> None:
        '''Method that is called on each clock tick, where any number of agent actions can be initiated. The full
        list of agent actions can be found at https://github.com/NateRex/malmoext/blob/master/docs/agent_actions.md

        The actions performed by an agent may depend on the current game state. Documentation on what state details
        are observable can be found at https://github.com/NateRex/malmoext/blob/master/docs/scenario_state.md

        Example implementation:
            
            agent = getAgent()

            mob = agent.closest_hostile_mob()

            if mob != None:
            
                if agent.lookAt(mob) and agent.moveTo(mob):
                
                    agent.attack()

            else:
            
                agent.doNothing()
        '''
        pass
    

    def run(self, ports=[10000]) -> None:
        '''Executes this scenario within the Malmo Minecraft instances running on the given ports. By default, a single
        Malmo Minecraft instance running on port 10000 is assumed.
        
        Documentation on how to run one or more Malmo Minecraft instances on different ports can be found at
        https://github.com/NateRex/malmoext/blob/master/README.md#running-a-scenario
        '''

        # Initialize Malmo Platform environment
        MalmoBootstrap.init_env()

        # Construct scenario
        self.build_scenario(self.__builder)

        # Validate scenario
        numAgents = len(self.__builder.agents)
        if (len(ports) < numAgents):
            raise Exception('Number of agents must not exceed the number of Malmo Minecraft instances currently running.')
        if (numAgents == 0):
            print('No agents present in scenario. Exiting.')
            exit(0)

        # Construct agents
        clientPool = MalmoPython.ClientPool()
        agentIdx = 0
        agentZero = None
        for builder in self.__builder.agents.values():
            agent = Agent(builder)
            self.__agents[agent.get_name()] = agent
            clientPool.add(MalmoPython.ClientInfo('127.0.0.1', ports[agentIdx]))
            if (agentZero is None):
                agentZero = agent
            agentIdx += 1

        # Load the scenario
        mission = MalmoPython.MissionSpec(self.__builder.build(), True)
        parse_command_line(agentZero.get_host())

        # Start the mission
        agentIdx = 0
        for agent in self.__agents.values():
            recordingObject = get_default_recording_object(agentZero.get_host(), "agent_{}_viewpoint_continuous".format(agentIdx + 1))
            self.__start_host_mission(agent, mission, clientPool, recordingObject, agentIdx, '')
            agentIdx += 1
        
        # Wait for mission to start
        self.__wait_for_mission_start()

        # While mission is running, repeatedly synchronize the local state with the remote server state,
        # and execute agent actions (assume the time limit is the same across all agents)
        while (agentZero.is_mission_active()):

            # Avoid handing off control while we are still waiting to receive observations for agents
            all_agents_have_observations = True
            for agent in self.__agents.values():
                num_observations = agent.get_host().peekWorldState().number_of_observations_since_last_state
                all_agents_have_observations = all_agents_have_observations and num_observations > 0
            if not all_agents_have_observations:
                continue

            # Sync agent states
            for agent in self.__agents.values():
                agent.sync()

            # Call handler to perform agent actions
            self.on_tick(self.__agents)
            time.sleep(0.05)

        print('Mission has ended.')


    def __start_host_mission(self, agent, mission, client_pool, recording, role, experimentId) -> None:
        '''Attempts to start a mission for an agent host. Will automatically retry on failure. After multiple,
        failures, an error will be reported and the program will exit.'''

        used_attempts = 0
        max_attempts = 5
        print("Starting mission for agent ", role)
        while True:
            try:
                agent.get_host().startMission(mission, client_pool, recording, role, experimentId)
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

    def __wait_for_mission_start(self) -> None:
        '''This method will block execution until all given hosts have succesfully started their mission. If any host
        fails to begin their mission, a timeout error will occur and the program will exit.'''
        print("Waiting for the mission to start", end=' ')
        agents = self.__agents.values()
        start_flags = [False for a in agents]
        start_time = time.time()
        time_out = 120  # Allow two minutes for mission to start.
        while not all(start_flags) and time.time() - start_time < time_out:
            states = [a.get_host().peekWorldState() for a in agents]
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