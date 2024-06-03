from malmoext import Scenario, Vector, Block, Mob, Item, Inventory

class KillingSpree(Scenario):
    '''Scenario where a computer agent repeatedly attacks the closest villager.'''

    def build_scenario(self, builder):
        
        # Metadata
        builder.set_description('Killing Spree')
        builder.set_time_limit(30)

        # Agents
        builder.add_agent('computer')
        builder.agents['computer'].set_position(Vector(0, 4, 0))
        builder.agents['computer'].add_inventory_item(Item.diamond_sword, Inventory.HotBar._0)

        # Mobs
        builder.world.add_mob(Mob.villager, Vector(8, 4, 8))
        builder.world.add_mob(Mob.villager, Vector(-8, 4, -8))
        builder.world.add_mob(Mob.villager, Vector(8, 4, -8))

        # Structures
        builder.world.add_line(Block.fence, Vector(-30, 4, -30), Vector(30, 4, -30))
        builder.world.add_line(Block.fence, Vector(30, 4, -30), Vector(30, 4, 30))
        builder.world.add_line(Block.fence, Vector(30, 4, 30), Vector(-30, 4, 30))
        builder.world.add_line(Block.fence, Vector(-30, 4, 30), Vector(-30, 4, -30))



    def on_tick(self, agents) -> None:

        # Agent actions
        closest_villager = agents['computer'].state.get_nearby_entity(Mob.villager)
        if closest_villager is not None:
            agents['computer'].attack(closest_villager)
        else:
            agents['computer'].do_nothing()

        


# Run scenario
scenario = KillingSpree().run(ports=[10000])