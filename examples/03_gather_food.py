from malmoext import Scenario, Vector, Block, Item, Inventory

class GatherFood(Scenario):
    '''Scenario where a computer agent gathers food items from the ground and returns them to a human player.
    The food items are strategically placed on the ground at the start of the scenario.'''

    def build_scenario(self, builder):
        
        # Metadata
        builder.set_description('Gather Food')
        builder.set_time_limit(30)

        # Agents (computer agent starts with 4 baked potatoes in their inventory, spread across two inventory slots)
        builder.add_agent('computer')
        builder.agents['computer'].set_position(Vector(0, 4, 0))
        builder.agents['computer'].add_inventory_item(Item.baked_potato, Inventory.HotBar._1, 1)
        builder.agents['computer'].add_inventory_item(Item.baked_potato, Inventory.HotBar._2, 3)

        builder.add_agent('human')
        builder.agents['human'].set_position(Vector(8, 4, 8))

        # Structures
        builder.world.add_line(Block.fence, Vector(-30, 4, -30), Vector(30, 4, -30))
        builder.world.add_line(Block.fence, Vector(30, 4, -30), Vector(30, 4, 30))
        builder.world.add_line(Block.fence, Vector(30, 4, 30), Vector(-30, 4, 30))
        builder.world.add_line(Block.fence, Vector(-30, 4, 30), Vector(-30, 4, -30))

        # Items
        # builder.world.add_item(Item.baked_potato, Vector(-8, 6, -8))
        # builder.world.add_item(Item.baked_potato, Vector(-8, 6, 8))
        # builder.world.add_item(Item.baked_potato, Vector(8, 6, -8))
        # builder.world.add_item(Item.diamond, Vector(8, 8, -8))



    def on_tick(self, agents) -> None:

        if agents['computer'].state.has_inventory_item(Item.baked_potato):
            # Agent has food. Give it to the human player.
            agents['computer'].give_item(Item.baked_potato, 'human')

        elif agents['computer'].state.has_nearby_entity(Item.baked_potato):
            # Food is lying nearby. Go and pick it up.
            agents['computer'].look_at(Item.baked_potato)
            agents['computer'].move_to(Item.baked_potato)

        else:
            # Nothing to do
            agents['computer'].do_nothing()




# Run scenario
scenario = GatherFood().run(ports=[10000, 10001])