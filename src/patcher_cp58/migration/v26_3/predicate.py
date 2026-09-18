from copy import deepcopy
from .lib import dict_cp58, rl_cp58
from . import number_provider
from ...datapack import DatapackResourceFormatError

def is_loot_condition( predicate: dict | list ) -> bool:
    if isinstance( predicate, dict ):
        s = dict_cp58.get_path( predicate, 'condition' )
        if isinstance( s, str ): return True
    elif isinstance( predicate, list ):
        return True
    return False

def wrap_loot_condition( terms: list | dict | str ) -> dict:
    output = {
        "type": "minecraft:all_of",
        "terms": []
    }
    if isinstance( terms, list ):
        l = len(terms)
        if l <= 0:
            dict_cp58.replace_path( output, 'terms', value=[] )
        elif l == 1:
            #term = convert_predicate( terms[0] )
            #dict_cp58.replace_path( output, 'terms', value=term )
            return convert_loot_condition( terms[0] )
        else:
            predicate_list = list()
            for p in terms:
                predicate_list.append( convert_loot_condition( p ) )
            dict_cp58.replace_path( output, 'terms', value=predicate_list )
    elif isinstance( terms, dict ):
        return convert_loot_condition( terms )
    else:
    #elif isinstance( terms, str ):
        dict_cp58.replace_path( output, 'terms', value=terms )
    return output

def convert_predicate( predicate: dict | list ) -> dict:
    if isinstance( predicate, list ):
        predicate = wrap_loot_condition( predicate )
    else:
        predicate = convert_loot_condition( predicate )
        if isinstance( predicate, str ):
            predicate = wrap_loot_condition( predicate )
    return predicate

def convert_loot_condition( predicate: dict | list ) -> dict:
    if not is_loot_condition( predicate ): 
        raise DatapackResourceFormatError( "PredicateFormatError" )
    if isinstance( predicate, list ):
        return wrap_loot_condition( predicate )

    output = {}
## "condition" -> "type"
    s = dict_cp58.get_path( predicate, 'condition' )
    del predicate['condition']
    dict_cp58.replace_path( output, 'type', value=s )

## loot_condition_type
    loot_condition_type = rl_cp58.namespaced( s )

# "all_of", "any_of"
    if loot_condition_type in ( "minecraft:all_of", "minecraft:any_of" ): 
        terms = dict_cp58.get_path( predicate, 'terms' )
        if terms == None: 
            dict_cp58.replace_path( output, 'terms', value=[] )
        elif isinstance( terms, list ):
            l = len(terms)
            if l <= 0:
                dict_cp58.replace_path( output, 'terms', value=[] )
            elif l == 1:
                term = convert_loot_condition( terms[0] )
                dict_cp58.replace_path( output, 'terms', value=term )
            else:
                predicate_list = list()
                for p in terms:
                    predicate_list.append( convert_loot_condition( p ) )
                dict_cp58.replace_path( output, 'terms', value=predicate_list )

# "block_state_property" -> "match_block"
    elif loot_condition_type == "minecraft:block_state_property":
        dict_cp58.replace_path( output, 'type', value='minecraft:match_block' )
        dict_cp58.copy_path( output, 'blocks', predicate, 'block' )
        dict_cp58.copy_path( output, 'state', predicate, 'properties' )

# "damage_source_properties"
    elif loot_condition_type == "minecraft:damage_source_properties":
        damage_type_predicate = dict_cp58.get_path( predicate, 'predicate' )
        if isinstance( damage_type_predicate, dict ):
            damage_type_predicate = convert_damage_type_predicate( damage_type_predicate )
            dict_cp58.replace_path( output, 'predicate', value=damage_type_predicate )

# "enchantment_active_check"
    elif loot_condition_type == "minecraft:enchantment_active_check":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'active', predicate, 'active' )

# "entity_properties"
    elif loot_condition_type == "minecraft:entity_properties":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'entity', predicate, 'entity' )
        entity_predicate = dict_cp58.get_path( predicate, 'predicate' )
        if entity_predicate is not None:
            entity_predicate = convert_entity_predicate( entity_predicate )
            dict_cp58.replace_path( output, 'predicate', value=entity_predicate )

# "entity_scores"
    elif loot_condition_type == "minecraft:entity_scores":
        dict_cp58.copy_path( output, 'entity', predicate, 'entity' )
        scores = dict_cp58.get_path( predicate, 'scores' )
        if isinstance( scores, dict ):
            scores_dict = {}
            for objective in scores:
                range = number_provider.convert_value_range( scores[objective] )
                if range is not None:
                    scores_dict[objective] = range
            dict_cp58.replace_path( output, 'scores', value=scores_dict )

# "environment_attribute_check"
    elif loot_condition_type == "minecraft:environment_attribute_check":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'attribute', predicate, 'attribute' )
        dict_cp58.copy_path( output, 'value', predicate, 'value' )

# "inverted"
    elif loot_condition_type == "minecraft:inverted":
        term = dict_cp58.get_path( predicate, 'term' )
        if isinstance( term, dict ):
            term = convert_loot_condition( term )
        dict_cp58.replace_path( output, 'term', value=term )

# "killed_by_player"
    elif loot_condition_type == "minecraft:killed_by_player":
        pass

# "location_check"
    elif loot_condition_type == "minecraft:location_check":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'offsetX', predicate, 'offsetX' )
        dict_cp58.copy_path( output, 'offsetY', predicate, 'offsetY' )
        dict_cp58.copy_path( output, 'offsetZ', predicate, 'offsetZ' )
        location_predicate = dict_cp58.get_path( predicate, 'predicate' )
        if location_predicate is not None:
            location_predicate = convert_location_predicate( location_predicate )
            dict_cp58.replace_path( output, 'predicate', value=location_predicate )

# "match_tool"
    elif loot_condition_type == "minecraft:match_tool":
        #output.update( deepcopy( predicate ) )
        item_predicate = dict_cp58.get_path( predicate, 'predicate' )
        if item_predicate is not None:
            item_predicate = convert_item_predicate( item_predicate )
            dict_cp58.replace_path( output, 'predicate', value=item_predicate )

# "random_chance"
    elif loot_condition_type == "minecraft:random_chance":
        chance = dict_cp58.get_path( predicate, 'chance' )
        if chance is not None:
            chance = number_provider.convert_float_provider( chance )
            dict_cp58.replace_path( output, 'chance', value=chance )

# "random_chance_with_enchanted_bonus"
    elif loot_condition_type == "minecraft:random_chance_with_enchanted_bonus":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'enchantment', predicate, 'enchantment' )
        dict_cp58.copy_path( output, 'enchanted_chance', predicate, 'enchanted_chance' )
        dict_cp58.copy_path( output, 'unenchanted_chance', predicate, 'unenchanted_chance' )

# "reference"
    elif loot_condition_type == "minecraft:reference":
        predicate_id = dict_cp58.get_path( predicate, 'name' )
        if predicate_id is not None:
            output = predicate_id

# "survives_explosion"
    elif loot_condition_type == "minecraft:survives_explosion":
        pass

# "table_bonus"
    elif loot_condition_type == "minecraft:table_bonus":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'enchantment', predicate, 'enchantment' )
        dict_cp58.copy_path( output, 'chances', predicate, 'chances' )

# "time_check"
    elif loot_condition_type == "minecraft:time_check":
        dict_cp58.copy_path( output, 'clock', predicate, 'clock' )
        dict_cp58.copy_path( output, 'period', predicate, 'period' )
        value_range = dict_cp58.get_path( predicate, 'value' )
        if value_range is not None:
            value_range = number_provider.convert_value_range( value_range )
            dict_cp58.replace_path( output, 'value', value=value_range )

# "value_check" -> "int_value_check"
    elif loot_condition_type == "minecraft:value_check":
        dict_cp58.replace_path( output, 'type', value='minecraft:int_value_check' )
        value = dict_cp58.get_path( predicate, 'value' )
        if value is not None:
            value = number_provider.convert_int_provider( value )
            dict_cp58.replace_path( output, 'value', value=value )
        value_range = dict_cp58.get_path( predicate, 'range' )
        if value_range is not None:
            value_range = number_provider.convert_value_range( value_range )
            dict_cp58.replace_path( output, 'test', value=value_range )

# "weather_check"
    elif loot_condition_type == "minecraft:weather_check":
        #output.update( deepcopy( predicate ) )
        dict_cp58.copy_path( output, 'raining', predicate, 'raining' )
        dict_cp58.copy_path( output, 'thundering', predicate, 'thundering' )

# EXCEPTION
    else:
        output.update( deepcopy( predicate ) )
##
    return output



def convert_entity_predicate( entity:dict ) -> dict:
    if not isinstance( entity, dict ):
        return entity
    output = {}
    for key in [str(key) for key in entity.keys()]:
        sub_predicate_type = rl_cp58.namespaced( key )
        if sub_predicate_type in (
            "minecraft:location",
            "minecraft:stepping_on",
            "minecraft:movement_affected_by"
        ):
            output[key] = convert_location_predicate(entity[key])
        elif sub_predicate_type in (
            "minecraft:vehicle",
            "minecraft:passenger",
            "minecraft:targeted_entity"
        ):
            output[key] = convert_entity_predicate(entity[key])
        elif sub_predicate_type in (
            "minecraft:slots",
            "minecraft:equipment"
        ) and isinstance( entity[key], dict ) :
            output[key] = {}
            for slot in [str(key) for key in entity[key].keys() ]:
                output[key][slot] = convert_item_predicate(entity[key][slot])
        elif sub_predicate_type == "minecraft:type_specific/lightning":
            output[key] = {}
            dict_cp58.copy_path( output, key, entity, 'blocks_set_on_fire' )
            p = dict_cp58.get_path( entity, key, 'entity_struck' )
            if p is not None:
                output[key]['entity_struck'] = convert_entity_predicate( p )
        elif sub_predicate_type == "minecraft:type_specific/player":
            output[key] = {}
            for player_predicate_type in [str(key) for key in entity[key].keys() ]:
                if player_predicate_type == 'looking_at':
                    output[key]['looking_at'] = convert_entity_predicate( entity[key]['looking_at'] )
                else:
                    output[key][player_predicate_type] = deepcopy( entity[key][player_predicate_type] )
        else:
            output[key] = deepcopy( entity[key] )
##
    return output


def convert_location_predicate( location:dict ) -> dict:
    if not isinstance( location, dict ):
        return location
    output = {}
    for key in [str(key) for key in location.keys()]:
        if key == "block":
            output[key] = convert_block_predicate(location[key])
        else:
            output[key] = deepcopy( location[key] )
##
    return output

def convert_block_predicate( block_predicate:dict ) -> dict:
    if not isinstance( block_predicate, dict ):
        return block_predicate
    output = {}
    for key in [str(key) for key in block_predicate.keys()]:
        output[key] = deepcopy( block_predicate[key] )
##
    return output


def convert_item_predicate( item_predicate:dict ) -> dict:
    if not isinstance( item_predicate, dict ):
        return item_predicate
    output = {}
    for key in [str(key) for key in item_predicate.keys()]:
        if key == "predicates":
            output['predicates'] = {}
            for s in [str(key) for key in item_predicate['predicates'].keys()]:
                component_predicate_type = rl_cp58.namespaced( s )
            # "bundle_contents"
                if component_predicate_type == "minecraft:bundle_contents":
                # size
                    dict_cp58.copy_path( output, ( 'predicates', s, 'items', 'size' ), item_predicate, ( 'predicates', s, 'items', 'size' ) )
                # contains
                    contains = dict_cp58.get_path( item_predicate, 'predicates', s, 'items', 'contains' )
                    if isinstance( contains, list ):
                        item_predicate_list = []
                        for p in contains:
                            item_predicate_list.append( convert_item_predicate( p ) )
                        dict_cp58.replace_path( output, 'predicates', s, 'items', 'contains', value=item_predicate_list )
                # count
                    count = dict_cp58.get_path( item_predicate, 'predicates', s, 'items', 'count' )
                    if isinstance( count, list ):
                        count_list = []
                        for c in count:
                            if isinstance( c, dict ):
                                count_list.append( {} )
                                p = dict_cp58.get_path( c, 'test' )
                                if isinstance( p, dict ):
                                    p = convert_item_predicate( p )
                                    dict_cp58.replace_path( count_list[-1], 'test', value=p )
                                dict_cp58.copy_path( count_list[-1], 'count', c, 'count' )
                            else:
                                count_list.append( c )
                        dict_cp58.replace_path( output, 'predicates', s, 'items', 'count', value=count_list )
            # "potion_contents"
                if component_predicate_type == "minecraft:potion_contents":
                    potion_contents = { "potions": [] }
                    potion_contents['potions'] = deepcopy( item_predicate['predicates'][s] )
                    output['predicates'][s] = potion_contents
            #
                else:
                    output['predicates'][s] = deepcopy( item_predicate['predicates'][s] )
        else:
            output[key] = deepcopy( item_predicate[key] )
##
    return output


def convert_damage_predicate( damage:dict ) -> dict:
    output = {}
    dict_cp58.copy_path( output, 'blocked', damage, 'blocked' )
    dict_cp58.copy_path( output, 'dealt', damage, 'dealt' )
    dict_cp58.copy_path( output, 'taken', damage, 'taken' )
    entity_predicate = dict_cp58.get_path( damage, 'source_entity' )
    if entity_predicate is not None:
        entity_predicate = convert_entity_predicate( entity_predicate )
        dict_cp58.replace_path( output, 'source_entity', value=entity_predicate )
    damage_type = dict_cp58.get_path( damage, 'type' )
    if damage_type is not None:
        damage_type = convert_damage_type_predicate( damage_type )
        dict_cp58.replace_path( output, 'type', value=damage_type )
##
    return output


def convert_damage_type_predicate( damage_source:dict ) -> dict:
    output = {}
    dict_cp58.copy_path( output, 'is_direct', damage_source, 'is_direct' )
    entity_predicate = dict_cp58.get_path( damage_source, 'direct_entity' )
    if entity_predicate is not None:
        entity_predicate = convert_entity_predicate( entity_predicate )
        dict_cp58.replace_path( output, 'direct_entity', value=entity_predicate )
    entity_predicate = dict_cp58.get_path( damage_source, 'source_entity' )
    if entity_predicate is not None:
        entity_predicate = convert_entity_predicate( entity_predicate )
        dict_cp58.replace_path( output, 'source_entity', value=entity_predicate )
    damage_source_tags = dict_cp58.get_path( damage_source, 'tags' )
    if isinstance( damage_source_tags, list ):
        damage_type_tags_list = list()
        for damage_tag in damage_source_tags:
            damage_type_tags_list.append(dict())
            damage_type_tags_id = dict_cp58.get_path( damage_tag, 'id' )
            if isinstance( damage_type_tags_id, str ):
                damage_type_tags_list[-1]['id'] = f'#{damage_type_tags_id}'
            dict_cp58.copy_path( damage_type_tags_list[-1], 'expected', damage_tag, 'expected' )
        dict_cp58.replace_path( output, 'tags', value=damage_type_tags_list )
##
    return output
