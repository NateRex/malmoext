from malmoext import Scenario, Vector, Block

class FollowMe(Scenario):
    '''Simple scenario where a computer agent follows a human player for 30 seconds.'''

    def build_scenario(self, builder):
        
        # Metadata
        builder.set_description('Follow Me')
        builder.set_time_limit(30)

        # Agents
        builder.add_agent('computer')
        builder.agents['computer'].set_position(Vector(0, 4, 0))
        builder.add_agent('human')
        builder.agents['human'].set_position(Vector(10, 4, 10))

        # Structures
        builder.world.add_line(Block.fence, Vector(-30, 4, -30), Vector(30, 4, -30))
        builder.world.add_line(Block.fence, Vector(30, 4, -30), Vector(30, 4, 30))
        builder.world.add_line(Block.fence, Vector(30, 4, 30), Vector(-30, 4, 30))
        builder.world.add_line(Block.fence, Vector(-30, 4, 30), Vector(-30, 4, -30))



    def on_tick(self, agents) -> None:

        # Agent actions
        agents['computer'].look_at('human')
        agents['computer'].move_to('human', keep_distance=3)
        



# Run scenario
scenario = FollowMe().run(ports=[10000, 10001])