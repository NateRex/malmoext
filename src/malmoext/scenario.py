import malmo.MalmoPython as MalmoPython

class Scenario:

    def __init__(self):
        print('hello world')



    def on_tick(self):
        '''Method that is called on each clock tick, where any number of agent actions can be initiated. The full
        list of agent actions is available at https://github.com/NateRex/malmoext/docs/agent_actions.md

        The actions performed by an agent may depend on the current game state. Documentation on what state details
        are available can be found at https://github.com/NateRex/malmoext/docs/agent_state.md

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
    