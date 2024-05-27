from typing import Union
from enum import Enum

class ReflectiveEnum(Enum):
    '''An enumerated type that provides additional utility methods for checking
    whether keys or values exist within the enum'''

    @classmethod
    def contains(cls, toCheck):
        '''Returns true if the given string is a member of this enum'''
        if isinstance(toCheck, str) or isinstance(toCheck, int):
            return toCheck in cls._value2member_map_
        else:
            return toCheck.value in cls._value2member_map_



class TimeOfDay(ReflectiveEnum):
    '''Enum type describing unique times of day within Minecraft'''

    dawn = 0
    noon = 6000
    sunset = 12000
    midnight = 18000



class Direction(ReflectiveEnum):
    '''Enum type describing compass directions in Minecraft'''

    north = 180
    east = -90
    south = 0
    west = 90



class Inventory:
    '''Enumerations describing inventory slot locations'''

    class HotBar(ReflectiveEnum):
        '''An inventory hotbar slot'''

        _0 = 0
        _1 = 1
        _2 = 2
        _3 = 3
        _4 = 4
        _5 = 5
        _6 = 6
        _7 = 7
        _8 = 8

    class Main(ReflectiveEnum):
        '''A main player inventory slot. This does NOT include hot bar inventory.'''

        _9 = 9
        _10 = 10
        _11 = 11
        _12 = 12
        _13 = 13
        _14 = 14
        _15 = 15
        _16 = 16
        _17 = 17
        _18 = 18
        _19 = 19
        _20 = 20
        _21 = 21
        _22 = 22
        _23 = 23
        _24 = 24
        _25 = 25
        _26 = 26
        _27 = 27
        _28 = 28
        _29 = 29
        _30 = 30
        _31 = 31
        _32 = 32
        _33 = 33
        _34 = 34
        _35 = 35

    class Armor(ReflectiveEnum):
        '''An inventory slot used to equip pieces of armor'''

        boots = 36
        leggings = 37
        chestplate = 38
        helmet = 39


class Mob(ReflectiveEnum):
    '''A Minecraft mob entity'''

    agent = "Agent"
    bat = "Bat"
    blaze = "Blaze"
    cave_spider = "CaveSpider"
    chicken = "Chicken"
    cow = "Cow"
    creeper = "Creeper"
    donkey = "Donkey"
    elder_guardian = "ElderGuardian"
    ender_dragon = "EnderDragon"
    enderman = "Enderman"
    endermite = "Endermite"
    evocation_villager = "EvocationIllager"           # Malmo has typo, which needs to be replicated here
    ghast = "Ghast"
    giant = "Giant"
    guardian = "Guardian"
    horse = "Horse"
    husk = "Husk"
    lava_slime = "LavaSlime"
    llama = "Llama"
    mule = "Mule"
    mushroom_cow = "MushroomCow"
    ozelot = "Ozelot"
    pig = "Pig"
    pig_zombie = "PigZombie"
    polar_bear = "PolarBear"
    rabbit = "Rabbit"
    sheep = "Sheep"
    shulker = "Shulker"
    silverfish = "Silverfish"
    skeleton = "Skeleton"
    skeleton_horse = "SkeletonHorse"
    slime = "Slime"
    snowman = "SnowMan"
    spider = "Spider"
    squid = "Squid"
    stray = "Stray"
    vex = "Vex"
    villager = "Villager"
    villager_golem = "VillagerGolem"
    vindication_villager = "VindicationIllager"     # Malmo has typo, which needs to be replicated here
    witch = "Witch"
    wither_boss = "WitherBoss"
    wither_skeleton = "WitherSkeleton"
    wolf = "Wolf"
    zombie = "Zombie"
    zombie_horse = "ZombieHorse"
    zombie_villager = "ZombieVillager"

    @classmethod
    def is_hostile(cls, to_check):
        return to_check in HOSTILE_MOBS
    
    @classmethod
    def is_peaceful(cls, to_check):
        return to_check in PEACEFUL_MOBS
    
    @classmethod
    def drops_food(cls, to_check):
        return to_check in FOOD_MOBS

HOSTILE_MOBS = set([
    Mob.blaze,
    Mob.cave_spider,
    Mob.creeper,
    Mob.elder_guardian,
    Mob.ender_dragon,
    Mob.enderman,
    Mob.endermite,
    Mob.evocation_villager,
    Mob.ghast,
    Mob.guardian,
    Mob.husk,
    Mob.lava_slime,
    Mob.pig_zombie,
    Mob.shulker,
    Mob.silverfish,
    Mob.skeleton,
    Mob.slime,
    Mob.spider,
    Mob.stray,
    Mob.vex,
    Mob.vindication_villager,
    Mob.witch,
    Mob.wither_boss,
    Mob.wither_skeleton,
    Mob.zombie,
    Mob.zombie_villager
])

PEACEFUL_MOBS = set([
    Mob.bat,
    Mob.chicken,
    Mob.cow,
    Mob.donkey,
    Mob.giant,
    Mob.horse,
    Mob.llama,
    Mob.mule,
    Mob.mushroom_cow,
    Mob.ozelot,
    Mob.pig,
    Mob.polar_bear,
    Mob.rabbit,
    Mob.sheep,
    Mob.skeleton_horse,
    Mob.snowman,
    Mob.squid,
    Mob.villager,
    Mob.villager_golem,
    Mob.wolf,
    Mob.zombie_horse
])

FOOD_MOBS = set([
    Mob.chicken,
    Mob.cow,
    Mob.mushroom_cow,
    Mob.pig,
    Mob.rabbit,
    Mob.sheep
])



class Item(ReflectiveEnum):
    '''A Minecraft item'''

    acacia_boat = "acacia_boat"
    acacia_door = "acacia_door"
    apple = "apple"
    armor_stand = "armor_stand"
    arrow = "arrow"
    baked_potato = "baked_potato"
    banner = "banner"
    bed = "bed"
    beef = "beef"
    beetroot = "beetroot"
    beetroot_seeds = "beetroot_seeds"
    beetroot_soup = "beetroot_soup"
    birch_boat = "birch_boat"
    birch_door = "birch_door"
    blaze_powder = "blaze_powder"
    blaze_rod = "blaze_rod"
    boat = "boat"
    bone = "bone"
    book = "book"
    bow = "bow"
    bowl = "bowl"
    bread = "bread"
    brewing_stand = "brewing_stand"
    brick = "brick"
    bucket = "bucket"
    cake = "cake"
    carrot = "carrot"
    carrot_on_a_stick = "carrot_on_a_stick"
    cauldron = "cauldron"
    chainmail_boots = "chainmail_boots"
    chainmail_chestplate = "chainmail_chestplate"
    chainmail_helmet = "chainmail_helmet"
    chainmail_leggings = "chainmail_leggings"
    chest_minecart = "chest_minecart"
    chicken = "chicken"
    chorus_fruit = "chorus_fruit"
    chorus_fruit_popped = "chorus_fruit_popped"
    clay_ball = "clay_ball"
    clock = "clock"
    coal = "coal"
    command_block_minecart = "command_block_minecart"
    comparator = "comparator"
    compass = "compass"
    cooked_beef = "cooked_beef"
    cooked_chicken = "cooked_chicken"
    cooked_fish = "cooked_fish"
    cooked_mutton = "cooked_mutton"
    cooked_porkchop = "cooked_porkchop"
    cooked_rabbit = "cooked_rabbit"
    cookie = "cookie"
    dark_oak_boat = "dark_oak_boat"
    dark_oak_door = "dark_oak_door"
    diamond = "diamond"
    diamond_axe = "diamond_axe"
    diamond_boots = "diamond_boots"
    diamond_chestplate = "diamond_chestplate"
    diamond_helmet = "diamond_helmet"
    diamond_hoe = "diamond_hoe"
    diamond_horse_armor = "diamond_horse_armor"
    diamond_leggings = "diamond_leggings"
    diamond_pickaxe = "diamond_pickaxe"
    diamond_shovel = "diamond_shovel"
    diamond_sword = "diamond_sword"
    dragon_breath = "dragon_breath"
    dye = "dye"
    egg = "egg"
    elytra = "elytra"
    emerald = "emerald"
    enchanted_book = "enchanted_book"
    ender_eye = "ender_eye"
    ender_pearl = "ender_pearl"
    experience_bottle = "experience_bottle"
    feather = "feather"
    fermented_spider_eye = "fermented_spider_eye"
    filled_map = "filled_map"
    fire_charge = "fire_charge"
    firework_charge = "firework_charge"
    fireworks = "fireworks"
    fish = "fish"
    fishing_rod = "fishing_rod"
    flint = "flint"
    flint_and_steel = "flint_and_steel"
    flower_pot = "flower_pot"
    furnace_minecart = "furnace_minecart"
    ghast_tear = "ghast_tear"
    glass_bottle = "glass_bottle"
    glowstone_dust = "glowstone_dust"
    gold_ingot = "gold_ingot"
    gold_nugget = "gold_nugget"
    golden_apple = "golden_apple"
    golden_axe = "golden_axe"
    golden_boots = "golden_boots"
    golden_carrot = "golden_carrot"
    golden_chestplate = "golden_chestplate"
    golden_helmet = "golden_helmet"
    golden_hoe = "golden_hoe"
    golden_horse_armor = "golden_horse_armor"
    golden_leggings = "golden_leggings"
    golden_pickaxe = "golden_pickaxe"
    golden_shovel = "golden_shovel"
    golden_sword = "golden_sword"
    gunpowder = "gunpowder"
    hopper_minecart = "hopper_minecart"
    iron_axe = "iron_axe"
    iron_boots = "iron_boots"
    iron_chestplate = "iron_chestplate"
    iron_door = "iron_door"
    iron_helmet = "iron_helmet"
    iron_hoe = "iron_hoe"
    iron_horse_armor = "iron_horse_armor"
    iron_ingot = "iron_ingot"
    iron_leggings = "iron_leggings"
    iron_nugget = "iron_nugget"
    iron_pickaxe = "iron_pickaxe"
    iron_shovel = "iron_shovel"
    iron_sword = "iron_sword"
    item_frame = "item_frame"
    jungle_boat = "jungle_boat"
    jungle_door = "jungle_door"
    lava_bucket = "lava_bucket"
    lead = "lead"
    leather = "leather"
    leather_boots = "leather_boots"
    leather_chestplate = "leather_chestplate"
    leather_helmet = "leather_helmet"
    leather_leggings = "leather_leggings"
    lingering_potion = "lingering_potion"
    magma_cream = "magma_cream"
    map = "map"
    melon = "melon"
    melon_seeds = "melon_seeds"
    milk_bucket = "milk_bucket"
    minecart = "minecart"
    mushroom_stew = "mushroom_stew"
    mutton = "mutton"
    name_tag = "name_tag"
    nether_star = "nether_star"
    nether_wart = "nether_wart"
    netherbrick = "netherbrick"
    painting = "painting"
    paper = "paper"
    poisonous_potato = "poisonous_potato"
    porkchop = "porkchop"
    potato = "potato"
    potion = "potion"
    prismarine_crystals = "prismarine_crystals"
    prismarine_shard = "prismarine_shard"
    pumpkin_pie = "pumpkin_pie"
    pumpkin_seeds = "pumpkin_seeds"
    quartz = "quartz"
    rabbit = "rabbit"
    rabbit_foot = "rabbit_foot"
    rabbit_hide = "rabbit_hide"
    rabbit_stew = "rabbit_stew"
    record_11 = "record_11"
    record_13 = "record_13"
    record_blocks = "record_blocks"
    record_cat = "record_cat"
    record_chirp = "record_chirp"
    record_far = "record_far"
    record_mall = "record_mall"
    record_mellohi = "record_mellohi"
    record_stal = "record_stal"
    record_strad = "record_strad"
    record_wait = "record_wait"
    record_ward = "record_ward"
    redstone = "redstone"
    reeds = "reeds"
    repeater = "repeater"
    rotten_flesh = "rotten_flesh"
    saddle = "saddle"
    shears = "shears"
    shield = "shield"
    shulker_shell = "shulker_shell"
    sign = "sign"
    skull = "skull"
    slime_ball = "slime_ball"
    snowball = "snowball"
    spawn_egg = "spawn_egg"
    speckled_melon = "speckled_melon"
    spectral_arrow = "spectral_arrow"
    spider_eye = "spider_eye"
    splash_potion = "splash_potion"
    spruce_boat = "spruce_boat"
    spruce_door = "spruce_door"
    stick = "stick"
    stone_axe = "stone_axe"
    stone_hoe = "stone_hoe"
    stone_pickaxe = "stone_pickaxe"
    stone_shovel = "stone_shovel"
    stone_sword = "stone_sword"
    string = "string"
    sugar = "sugar"
    tipped_arrow = "tipped_arrow"
    tnt_minecart = "tnt_minecart"
    totem_of_undying = "totem_of_undying"
    water_bucket = "water_bucket"
    wheat = "wheat"
    wheat_seeds = "wheat_seeds"
    wooden_axe = "wooden_axe"
    wooden_door = "wooden_door"
    wooden_hoe = "wooden_hoe"
    wooden_pickaxe = "wooden_pickaxe"
    wooden_shovel = "wooden_shovel"
    wooden_sword = "wooden_sword"
    writable_book = "writable_book"
    written_book = "written_book"

    @classmethod
    def is_food(cls, to_check):
        return to_check in FOOD_ITEMS

FOOD_ITEMS = set([
    Item.apple,
    Item.baked_potato,
    Item.beef,
    Item.beetroot_soup,
    Item.bread,
    Item.cake,
    Item.carrot,
    Item.chicken,
    Item.cooked_beef,
    Item.cooked_chicken,
    Item.cooked_fish,
    Item.cooked_mutton,
    Item.cooked_porkchop,
    Item.cooked_rabbit,
    Item.cookie,
    Item.fish,
    Item.golden_apple,
    Item.golden_carrot,
    Item.mushroom_stew,
    Item.mutton,
    Item.poisonous_potato,
    Item.porkchop,
    Item.potato,
    Item.pumpkin_pie,
    Item.rabbit,
    Item.rabbit_stew,
    Item.rotten_flesh
])



class Block(ReflectiveEnum):
    '''A type of Minecraft block'''

    acacia_door = "acacia_door"
    acacia_fence = "acacia_fence"
    acacia_fence_gate = "acacia_fence_gate"
    acacia_stairs = "acacia_stairs"
    activator_rail = "activator_rail"
    air = "air"
    anvil = "anvil"
    barrier = "barrier"
    beacon = "beacon"
    bed = "bed"
    bedrock = "bedrock"
    beetroots = "beetroots"
    birch_door = "birch_door"
    birch_fence = "birch_fence"
    birch_fence_gate = "birch_fence_gate"
    birch_stairs = "birch_stairs"
    black_shulker_box = "black_shulker_box"
    blue_shulker_box = "blue_shulker_box"
    bone_block = "bone_block"
    bookshelf = "bookshelf"
    brewing_stand = "brewing_stand"
    brick_block = "brick_block"
    brick_stairs = "brick_stairs"
    brown_mushroom = "brown_mushroom"
    brown_mushroom_block = "brown_mushroom_block"
    brown_shulker_box = "brown_shulker_box"
    cactus = "cactus"
    cake = "cake"
    carpet = "carpet"
    carrots = "carrots"
    cauldron = "cauldron"
    chain_command_block = "chain_command_block"
    chest = "chest"
    chorus_flower = "chorus_flower"
    chorus_plant = "chorus_plant"
    clay = "clay"
    coal_block = "coal_block"
    coal_ore = "coal_ore"
    cobblestone = "cobblestone"
    cobblestone_wall = "cobblestone_wall"
    cocoa = "cocoa"
    command_block = "command_block"
    crafting_table = "crafting_table"
    cyan_shulker_box = "cyan_shulker_box"
    dark_oak_door = "dark_oak_door"
    dark_oak_fence = "dark_oak_fence"
    dark_oak_fence_gate = "dark_oak_fence_gate"
    dark_oak_stairs = "dark_oak_stairs"
    daylight_detector = "daylight_detector"
    daylight_detector_inverted = "daylight_detector_inverted"
    deadbush = "deadbush"
    detector_rail = "detector_rail"
    diamond_block = "diamond_block"
    diamond_ore = "diamond_ore"
    dirt = "dirt"
    dispenser = "dispenser"
    double_plant = "double_plant"
    double_stone_slab = "double_stone_slab"
    double_stone_slab2 = "double_stone_slab2"
    double_wooden_slab = "double_wooden_slab"
    dragon_egg = "dragon_egg"
    dropper = "dropper"
    emerald_block = "emerald_block"
    emerald_ore = "emerald_ore"
    enchanting_table = "enchanting_table"
    end_bricks = "end_bricks"
    end_gateway = "end_gateway"
    end_portal = "end_portal"
    end_portal_frame = "end_portal_frame"
    end_rod = "end_rod"
    end_stone = "end_stone"
    ender_chest = "ender_chest"
    farmland = "farmland"
    fence = "fence"
    fence_gate = "fence_gate"
    fire = "fire"
    flower_pot = "flower_pot"
    flowing_lava = "flowing_lava"
    flowing_water = "flowing_water"
    frosted_ice = "frosted_ice"
    furnace = "furnace"
    glass = "glass"
    glass_pane = "glass_pane"
    glowstone = "glowstone"
    gold_block = "gold_block"
    gold_ore = "gold_ore"
    golden_rail = "golden_rail"
    grass = "grass"
    grass_path = "grass_path"
    gravel = "gravel"
    gray_shulker_box = "gray_shulker_box"
    green_shulker_box = "green_shulker_box"
    hardened_clay = "hardened_clay"
    hay_block = "hay_block"
    heavy_weighted_pressure_plate = "heavy_weighted_pressure_plate"
    hopper = "hopper"
    ice = "ice"
    iron_bars = "iron_bars"
    iron_block = "iron_block"
    iron_door = "iron_door"
    iron_ore = "iron_ore"
    iron_trapdoor = "iron_trapdoor"
    jukebox = "jukebox"
    jungle_door = "jungle_door"
    jungle_fence = "jungle_fence"
    jungle_fence_gate = "jungle_fence_gate"
    jungle_stairs = "jungle_stairs"
    ladder = "ladder"
    lapis_block = "lapis_block"
    lapis_ore = "lapis_ore"
    lava = "lava"
    leaves = "leaves"
    leaves2 = "leaves2"
    lever = "lever"
    light_blue_shulker_box = "light_blue_shulker_box"
    light_weighted_pressure_plate = "light_weighted_pressure_plate"
    lime_shulker_box = "lime_shulker_box"
    lit_furnace = "lit_furnace"
    lit_pumpkin = "lit_pumpkin"
    lit_redstone_lamp = "lit_redstone_lamp"
    lit_redstone_ore = "lit_redstone_ore"
    log = "log"
    log2 = "log2"
    magenta_shulker_box = "magenta_shulker_box"
    magma = "magma"
    melon_block = "melon_block"
    melon_stem = "melon_stem"
    mob_spawner = "mob_spawner"
    monster_egg = "monster_egg"
    mossy_cobblestone = "mossy_cobblestone"
    mycelium = "mycelium"
    nether_brick = "nether_brick"
    nether_brick_fence = "nether_brick_fence"
    nether_brick_stairs = "nether_brick_stairs"
    nether_wart = "nether_wart"
    nether_wart_block = "nether_wart_block"
    netherrack = "netherrack"
    noteblock = "noteblock"
    oak_stairs = "oak_stairs"
    observer = "observer"
    obsidian = "obsidian"
    orange_shulker_box = "orange_shulker_box"
    packed_ice = "packed_ice"
    pink_shulker_box = "pink_shulker_box"
    piston = "piston"
    piston_extension = "piston_extension"
    piston_head = "piston_head"
    planks = "planks"
    portal = "portal"
    potatoes = "potatoes"
    powered_comparator = "powered_comparator"
    powered_repeater = "powered_repeater"
    prismarine = "prismarine"
    pumpkin = "pumpkin"
    pumpkin_stem = "pumpkin_stem"
    purple_shulker_box = "purple_shulker_box"
    purpur_block = "purpur_block"
    purpur_double_slab = "purpur_double_slab"
    purpur_pillar = "purpur_pillar"
    purpur_slab = "purpur_slab"
    purpur_stairs = "purpur_stairs"
    quartz_block = "quartz_block"
    quartz_ore = "quartz_ore"
    quartz_stairs = "quartz_stairs"
    rail = "rail"
    red_flower = "red_flower"
    red_mushroom = "red_mushroom"
    red_mushroom_block = "red_mushroom_block"
    red_nether_brick = "red_nether_brick"
    red_sandstone = "red_sandstone"
    red_sandstone_stairs = "red_sandstone_stairs"
    red_shulker_box = "red_shulker_box"
    redstone_block = "redstone_block"
    redstone_lamp = "redstone_lamp"
    redstone_ore = "redstone_ore"
    redstone_torch = "redstone_torch"
    redstone_wire = "redstone_wire"
    reeds = "reeds"
    repeating_command_block = "repeating_command_block"
    sand = "sand"
    sandstone = "sandstone"
    sandstone_stairs = "sandstone_stairs"
    sapling = "sapling"
    sea_lantern = "sea_lantern"
    silver_shulker_box = "silver_shulker_box"
    skull = "skull"
    slime = "slime"
    snow = "snow"
    snow_layer = "snow_layer"
    soul_sand = "soul_sand"
    sponge = "sponge"
    spruce_door = "spruce_door"
    spruce_fence = "spruce_fence"
    spruce_fence_gate = "spruce_fence_gate"
    spruce_stairs = "spruce_stairs"
    stained_glass = "stained_glass"
    stained_glass_pane = "stained_glass_pane"
    stained_hardened_clay = "stained_hardened_clay"
    standing_banner = "standing_banner"
    standing_sign = "standing_sign"
    sticky_piston = "sticky_piston"
    stone = "stone"
    stone_brick_stairs = "stone_brick_stairs"
    stone_button = "stone_button"
    stone_pressure_plate = "stone_pressure_plate"
    stone_slab = "stone_slab"
    stone_slab2 = "stone_slab2"
    stone_stairs = "stone_stairs"
    stonebrick = "stonebrick"
    structure_block = "structure_block"
    structure_void = "structure_void"
    tallgrass = "tallgrass"
    tnt = "tnt"
    torch = "torch"
    trapdoor = "trapdoor"
    trapped_chest = "trapped_chest"
    tripwire = "tripwire"
    tripwire_hook = "tripwire_hook"
    unlit_redstone_torch = "unlit_redstone_torch"
    unpowered_comparator = "unpowered_comparator"
    unpowered_repeater = "unpowered_repeater"
    vine = "vine"
    wall_banner = "wall_banner"
    wall_sign = "wall_sign"
    water = "water"
    waterlily = "waterlily"
    web = "web"
    wheat = "wheat"
    white_shulker_box = "white_shulker_box"
    wooden_button = "wooden_button"
    wooden_door = "wooden_door"
    wooden_pressure_plate = "wooden_pressure_plate"
    wooden_slab = "wooden_slab"
    wool = "wool"
    yellow_flower = "yellow_flower"
    yellow_shulker_box = "yellow_shulker_box"


class Vector:
    '''A 3-dimensional vector'''

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Rotation:
    '''A rotation in yaw and pitch directions.'''

    def __init__(self, yaw: float, pitch: float):
        self.yaw = yaw
        self.pitch = pitch


class Entity:
    '''Metadata describing a mob, drop item, or an agent.'''

    def __init__(self, id: str, eType: Union[Mob, Item], name: str, position: Vector, quantity: int):
        self.id = id
        self.type = eType
        self.name = name
        self.position = position
        self.quantity = quantity


class InventoryItem:
    '''Representation of an item inside an agent's inventory'''

    def __init__(self, iType: Item, quantity: int, slot: Union[Inventory.HotBar, Inventory.Main, Inventory.Armor]):
        self.type = iType
        self.quantity = quantity
        self.slot = slot

