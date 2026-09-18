from copy import deepcopy
from .lib import dict_cp58, rl_cp58
from . import predicate, loot_table
from ...datapack import DatapackResourceFormatError

def is_advancement( advancement: dict ) -> bool:
    if isinstance( advancement, dict ):
        if dict_cp58.check_data_types( 
            advancement,
            {
                'criteria': dict
            }
        ):
            return True
    return False

def is_criterion( criterion: dict ) -> bool:
    if isinstance( criterion, dict ):
        s = dict_cp58.get_path( criterion, 'trigger' )
        if isinstance( s, str ): return True
        return True
    return False


def convert_advancement( advancement: dict ) -> dict:
    if not is_advancement( advancement ):
        raise DatapackResourceFormatError( "AdvancementFormatError" )
    output = {}

# "parent"
    dict_cp58.copy_path( output, 'parent', advancement, 'parent' )
# "display"
    dict_cp58.copy_path( output, 'display', advancement, 'display' )
# "criteria"
    criteria = dict_cp58.get_path( advancement, 'criteria' )
    if isinstance( criteria, dict ):
        dict_cp58.replace_path( output, 'criteria', value=dict() )
        for key, criterion in criteria.items():
            criterion = convert_criterion( criterion )
            dict_cp58.replace_path( output, 'criteria',key, value=criterion )
# "requirements"
    dict_cp58.copy_path( output, 'requirements', advancement, 'requirements' )
# "rewards"
    rewards = dict_cp58.get_path( advancement, 'rewards' )
    if isinstance( rewards, dict ):
        dict_cp58.replace_path( output, 'rewards', value=dict() )
        for reward_type, reward_value in rewards.items():
            if reward_type == 'loot':
                if isinstance( reward_value, str ):
                    dict_cp58.copy_path( output, ( 'rewards', reward_type ), rewards, reward_type )
                else:
                    reward_loot = loot_table.convert_loot_table( reward_value )
                    dict_cp58.replace_path( output, ( 'rewards', reward_type ), value=reward_loot )
            else:
                dict_cp58.copy_path( output, ( 'rewards', reward_type ), rewards, reward_type )
# "sends_telemetry_event"
    dict_cp58.copy_path( output, 'sends_telemetry_event', advancement, 'sends_telemetry_event' )
##
    return output

def convert_criterion( criterion: dict ) -> dict:
    if not is_criterion( criterion ):
        raise DatapackResourceFormatError( "AdvancementCriterionFormatError" )
    output = {}

# "trigger"
    s = dict_cp58.get_path( criterion, 'trigger' )
    #del criterion['trigger']
    dict_cp58.replace_path( output, 'trigger', value=s )
# "conditions"
    conditions = dict_cp58.get_path( criterion, 'conditions' )
    if conditions is not None:
        dict_cp58.replace_path( output, 'conditions', value=dict() )

## trigger_type
    trigger_type = rl_cp58.namespaced( s )

# "player" condition
    if trigger_type != "minecraft:impossible":
        update_entity_predicate( conditions, 'player', output )
        if dict_cp58.exist_path( conditions, 'player' ): del conditions['player']

# "location" condition
    if trigger_type in (
        "minecraft:allay_drop_item_on_block",
        "minecraft:any_block_use",
        "minecraft:default_block_use",
        "minecraft:item_used_on_block",
        "minecraft:placed_block"
    ):
        update_entity_predicate( conditions, 'location', output )
        if dict_cp58.exist_path( conditions, 'location' ): del conditions['location']

# no other conditions
    if trigger_type in (
        "minecraft:avoid_vibration",
        "minecraft:hero_of_the_village",
        "minecraft:impossible",
        "minecraft:location",
        "minecraft:slept_in_bed",
        "minecraft:started_riding",
        "minecraft:tick",
        "minecraft:voluntary_exile"
    ):
        pass

# no changes
#    elif trigger_type in ( ): output['conditions'].update( deepcopy( conditions ) )

# "bee_nest_destroyed"
    elif trigger_type == "minecraft:bee_nest_destroyed":
        dict_cp58.copy_path( output, ('conditions','blocks'), conditions, 'block' )
        update_item_predicate( conditions, 'item', output )
        dict_cp58.copy_path( output, ('conditions','num_bees_inside'), conditions, 'num_bees_inside' )

# "bred_animals"
    elif trigger_type == "minecraft:bred_animals":
        update_entity_predicate( conditions, 'child', output )
        update_entity_predicate( conditions, 'parent', output )
        update_entity_predicate( conditions, 'partner', output )

# "brewed_potion"
    elif trigger_type == "minecraft:brewed_potion":
        dict_cp58.copy_path( output, ('conditions','potion','potions'), conditions, 'potion' )

# "changed_dimension"
#    elif trigger_type == "minecraft:changed_dimension":

# "channeled_lightning"
    elif trigger_type == "minecraft:channeled_lightning":
        victims = dict_cp58.get_path( conditions, 'victims' )
        if isinstance( victims, list ):
            victim_list = list()
            for d in victims:
                victim_list.append( dict() )
                if isinstance( d, list ):
                    victim_list[-1] = predicate.convert_loot_condition( d )
                else:
                    victim_list[-1] = wrap_entity_predicate( d )
            dict_cp58.replace_path( output, 'conditions','victims', value=victim_list )

# "construct_beacon"
#    elif trigger_type == "minecraft:construct_beacon":

# "consume_item"
    elif trigger_type == "minecraft:consume_item":
        update_item_predicate( conditions, 'item', output )

# "crafter_recipe_crafted"
    elif trigger_type == "minecraft:crafter_recipe_crafted":
        dict_cp58.copy_path( output, ('conditions','recipes'), conditions, 'recipe_id' )
        update_item_predicate( conditions, 'ingredients', output )

# "cured_zombie_villager"
    elif trigger_type == "minecraft:cured_zombie_villager":
        update_entity_predicate( conditions, 'zombie', output )
        update_entity_predicate( conditions, 'villager', output )

# "effects_changed"
    elif trigger_type == "minecraft:effects_changed":
        dict_cp58.copy_path( output, ('conditions','effects'), conditions, 'effects' )
        update_entity_predicate( conditions, 'source', output )

# "enchanted_item"
    elif trigger_type == "minecraft:enchanted_item":
        update_item_predicate( conditions, 'item', output )
        dict_cp58.copy_path( output, ('conditions','levels'), conditions, 'levels' )

# "enter_block"
    elif trigger_type == "minecraft:enter_block":
        dict_cp58.copy_path( output, ('conditions','blocks'), conditions, 'block' )
        dict_cp58.copy_path( output, ('conditions','state'), conditions, 'state' )

# "entity_hurt_player"
    elif trigger_type == "minecraft:entity_hurt_player":
        update_damage_predicate( conditions, 'damage', output )

# "entity_killed_player"
    elif trigger_type == "minecraft:entity_killed_player":
        update_entity_predicate( conditions, 'entity', output )
        update_damage_source_predicate( conditions, 'killing_blow', output )

# "fall_after_explosion"
    elif trigger_type == "minecraft:fall_after_explosion":
        dict_cp58.copy_path( output, ('conditions','start_position'), conditions, 'start_position' )
        dict_cp58.copy_path( output, ('conditions','distance'), conditions, 'distance' )
        update_entity_predicate( conditions, 'cause', output )

# "fall_from_height"
#    elif trigger_type == "minecraft:fall_from_height":

# "filled_bucket"
    elif trigger_type == "minecraft:filled_bucket":
        update_item_predicate( conditions, 'item', output )

# "fishing_rod_hooked"
    elif trigger_type == "minecraft:fishing_rod_hooked":
        update_entity_predicate( conditions, 'entity', output )
        update_item_predicate( conditions, 'item', output )
        update_item_predicate( conditions, 'rod', output )

# "inventory_changed"
    elif trigger_type == "minecraft:inventory_changed":
        update_item_predicate( conditions, 'items', output )
        dict_cp58.copy_path( output, ('conditions','slots'), conditions, 'slots' )

# "item_durability_changed"
    elif trigger_type == "minecraft:item_durability_changed":
        update_item_predicate( conditions, 'items', output )
        dict_cp58.copy_path( output, ('conditions','delta'), conditions, 'delta' )
        dict_cp58.copy_path( output, ('conditions','durability'), conditions, 'durability' )

# "kill_mob_near_sculk_catalyst"
    elif trigger_type == "minecraft:kill_mob_near_sculk_catalyst":
        update_entity_predicate( conditions, 'entity', output )
        update_damage_source_predicate( conditions, 'killing_blow', output )

# "killed_by_arrow"
    elif trigger_type == "minecraft:killed_by_arrow":
        dict_cp58.copy_path( output, ('conditions','unique_entity_types'), conditions, 'unique_entity_types' )
        update_item_predicate( conditions, 'fired_from_weapon', output )
        victims = dict_cp58.get_path( conditions, 'victims' )
        if isinstance( victims, list ):
            victim_list = list()
            for d in victims:
                victim_list.append( dict() )
                if isinstance( d, list ):
                    victim_list[-1] = predicate.convert_loot_condition( d )
                else:
                    victim_list[-1] = wrap_entity_predicate( d )
            dict_cp58.replace_path( output, 'conditions','victims', value=victim_list )

# "levitation"
#    elif trigger_type == "minecraft:levitation":

# "lightning_strike"
    elif trigger_type == "minecraft:lightning_strike":
        update_entity_predicate( conditions, 'lightning', output )
        update_entity_predicate( conditions, 'bystander', output )

# "nether_travel"
#    elif trigger_type == "minecraft:nether_travel":

# "player_generates_container_loot"
    elif trigger_type == "minecraft:player_generates_container_loot":
        dict_cp58.copy_path( output, ('conditions','loot_tables'), conditions, 'loot_table' )

# "player_hurt_entity"
    elif trigger_type == "minecraft:player_hurt_entity":
        update_damage_predicate( conditions, 'damage', output )
        update_entity_predicate( conditions, 'entity', output )

# "player_interacted_with_entity"
    elif trigger_type == "minecraft:player_interacted_with_entity":
        update_item_predicate( conditions, 'item', output )
        update_entity_predicate( conditions, 'entity', output )

# "player_killed_entity"
    elif trigger_type == "minecraft:player_killed_entity":
        update_entity_predicate( conditions, 'entity', output )
        update_damage_source_predicate( conditions, 'killing_blow', output )

# "player_sheared_equipment"
    elif trigger_type == "minecraft:player_sheared_equipment":
        update_item_predicate( conditions, 'item', output )
        update_entity_predicate( conditions, 'entity', output )

# "recipe_crafted"
    elif trigger_type == "minecraft:recipe_crafted":
        dict_cp58.copy_path( output, ('conditions','recipes'), conditions, 'recipe_id' )
        update_item_predicate( conditions, 'ingredients', output )

# "recipe_unlocked"
    elif trigger_type == "minecraft:recipe_unlocked":
        dict_cp58.copy_path( output, ('conditions','recipes'), conditions, 'recipe' )

# "ride_entity_in_lava"
#    elif trigger_type == "minecraft:ride_entity_in_lava":

# "shot_crossbow"
    elif trigger_type == "minecraft:shot_crossbow":
        update_item_predicate( conditions, 'item', output )

# "slide_down_block"
    elif trigger_type == "minecraft:slide_down_block":
        dict_cp58.copy_path( output, ('conditions','blocks'), conditions, 'block' )
        dict_cp58.copy_path( output, ('conditions','state'), conditions, 'state' )

# "spear_mobs"
#    elif trigger_type == "minecraft:spear_mobs":

# "summoned_entity"
    elif trigger_type == "minecraft:summoned_entity":
        update_entity_predicate( conditions, 'entity', output )

# "tame_animal"
    elif trigger_type == "minecraft:tame_animal":
        update_entity_predicate( conditions, 'entity', output )

# "target_hit"
    elif trigger_type == "minecraft:target_hit":
        dict_cp58.copy_path( output, ('conditions','signal_strength'), conditions, 'signal_strength' )
        update_entity_predicate( conditions, 'projectile', output )

# "thrown_item_picked_up_by_entity"
    elif trigger_type == "minecraft:thrown_item_picked_up_by_entity":
        update_item_predicate( conditions, 'item', output )
        update_entity_predicate( conditions, 'entity', output )

# "thrown_item_picked_up_by_player"
    elif trigger_type == "minecraft:thrown_item_picked_up_by_player":
        update_item_predicate( conditions, 'item', output )
        update_entity_predicate( conditions, 'entity', output )

# "used_ender_eye"
#    elif trigger_type == "minecraft:used_ender_eye":

# "used_totem"
    elif trigger_type == "minecraft:used_totem":
        update_item_predicate( conditions, 'item', output )

# "using_item"
    elif trigger_type == "minecraft:using_item":
        update_item_predicate( conditions, 'item', output )

# "villager_trade"
    elif trigger_type == "minecraft:villager_trade":
        update_item_predicate( conditions, 'item', output )
        update_entity_predicate( conditions, 'villager', output )

# EXCEPTION
    else:
        if conditions is not None:
            output['conditions'].update( deepcopy( conditions ) )
##
    return output


def wrap_entity_predicate( entity_predicate:dict ) -> dict:
    if dict_cp58.exist_path( entity_predicate, 'condition' ):
        return predicate.convert_loot_condition( entity_predicate )
    output = {
        "type": "minecraft:entity_properties",
        "entity": "this",
        "predicate": {}
    }
    output['predicate'] = entity_predicate
    return output

def update_entity_predicate( conditions_dict: dict, source_path, target_dict: dict, target_path=None ):
    entity_predicate = dict_cp58.get_path( conditions_dict, source_path )
    if isinstance( entity_predicate, dict ):
        entity_predicate = wrap_entity_predicate( entity_predicate )
    elif isinstance( entity_predicate, list ):
        pass
    else: return
    if target_path is None:
        target_path = source_path
    condition = predicate.convert_loot_condition( entity_predicate )
    dict_cp58.replace_path( target_dict, ('conditions',target_path ), value=condition )

def update_damage_predicate( conditions_dict: dict, source_path, target_dict: dict, target_path=None ):
    damage_predicate = dict_cp58.get_path( conditions_dict, source_path )
    if damage_predicate is None: return
    if target_path is None:
        target_path = source_path
    condition = predicate.convert_damage_predicate( damage_predicate )
    dict_cp58.replace_path( target_dict, ('conditions',target_path ), value=condition )

def update_damage_source_predicate( conditions_dict: dict, source_path, target_dict: dict, target_path=None ):
    damage_source_predicate = dict_cp58.get_path( conditions_dict, source_path )
    if damage_source_predicate is None: return
    if target_path is None:
        target_path = source_path
    condition = predicate.convert_damage_type_predicate( damage_source_predicate )
    dict_cp58.replace_path( target_dict, ('conditions',target_path ), value=condition )

def update_item_predicate( conditions_dict: dict | list, source_path, target_dict: dict, target_path=None ):
    item_predicate = dict_cp58.get_path( conditions_dict, source_path )
    if target_path is None:
        target_path = source_path
    if isinstance( item_predicate, dict ):
        item_predicate = predicate.convert_item_predicate( item_predicate )
        dict_cp58.replace_path( target_dict, ('conditions',target_path ), value=item_predicate )
    elif isinstance( item_predicate, list ):
        item_predicate_list = list()
        for p in item_predicate:
            item_predicate_list.append( predicate.convert_item_predicate( p ) )
        dict_cp58.replace_path( target_dict, ('conditions',target_path ), value=item_predicate_list )
    else: return
