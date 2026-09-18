from copy import deepcopy
from .lib import dict_cp58, rl_cp58
from . import number_provider, predicate, item_modifier
from ...datapack import DatapackResourceFormatError

def is_loot_table( loot_table: dict ) -> bool:
    if isinstance( loot_table, dict ):
        #l = dict_cp58.get_path( loot_table, 'pools' )
        #if isinstance( l, list ): return True
        return True
    return False


def is_loot_pool( loot_pool: dict ) -> bool:
    if isinstance( loot_pool, dict ):
        rolls = dict_cp58.get_path( loot_pool, 'rolls' )
        if rolls is None : return False
        entries = dict_cp58.get_path( loot_pool, 'entries' )
        if isinstance( entries, list ) : return True
    return False


def is_loot_pool_entry( loot_pool_entry: dict ) -> bool:
    if isinstance( loot_pool_entry, dict ):
        s = dict_cp58.get_path( loot_pool_entry, 'type' )
        if isinstance( s, str ) : return True
    return False


def convert_loot_table( loot_table: dict ) -> dict:
    if not is_loot_table( loot_table ): 
        raise DatapackResourceFormatError( "LootTableFormatError" )
    output = {}
    for key in [str(key) for key in loot_table.keys()]:
        if key == "functions":
            functions = dict_cp58.get_path( loot_table, 'functions' )
            if isinstance( functions, list ):
                functions = item_modifier.convert_loot_function( functions, allow_list=True )
                dict_cp58.replace_path( output, 'modifier', value=functions )
        elif key == "pools":
            loot_pool_list = dict_cp58.get_path( loot_table, 'pools' )
            if isinstance( loot_pool_list, list ):
                dict_cp58.replace_path( output, 'pools', value=list() )
                for loot_pool in loot_pool_list:
                    loot_pool = convert_loot_pool( loot_pool )
                    output['pools'].append( loot_pool )
        else:
            dict_cp58.copy_path( output, key, loot_table, key )
##
    return output


def convert_loot_pool( loot_pool:dict ) -> dict:
    if not is_loot_pool( loot_pool ):
        raise DatapackResourceFormatError( "LootPoolFormatError" )
    output = {}

    for key in [str(key) for key in loot_pool.keys()]:
    # "rolls"
        if key == "rolls":
            rolls = dict_cp58.get_path( loot_pool, 'rolls' )
            rolls = number_provider.convert_int_provider( rolls )
            dict_cp58.replace_path( output, 'rolls', value=rolls )
    # "bonus_rolls"
        elif key == "bonus_rolls":
            bonus_rolls = dict_cp58.get_path( loot_pool, 'bonus_rolls' )
            bonus_rolls = number_provider.convert_float_provider( bonus_rolls )
            dict_cp58.replace_path( output, 'rolls', value=bonus_rolls )
    # "entries"
        elif key == "entries":
            loot_pool_entry_list = dict_cp58.get_path( loot_pool, 'entries' )
            if isinstance( loot_pool_entry_list, list ):
                dict_cp58.replace_path( output, 'entries', value=list() )
                for loot_pool_entry in loot_pool_entry_list:
                    loot_pool_entry = convert_loot_pool_entry( loot_pool_entry )
                    output['entries'].append( loot_pool_entry )
    # "functions" -> "modifier"
        elif key == "functions":
            functions = dict_cp58.get_path( loot_pool, 'functions' )
            if isinstance( functions, list ):
                functions = item_modifier.convert_loot_function( functions, allow_list=True )
                dict_cp58.replace_path( output, 'modifier', value=functions )
    # "conditions" -> "condition"
        elif key == "conditions":
            conditions = dict_cp58.get_path( loot_pool, 'conditions' )
            if isinstance( conditions, list ):
                conditions = predicate.convert_loot_condition( conditions )
                dict_cp58.replace_path( output, 'condition', value=conditions )
    # EXCEPTION
        else:
            dict_cp58.copy_path( output, key, loot_pool, key )
##
    return output


def convert_loot_pool_entry( loot_pool_entry:dict ) -> dict:
    if not is_loot_pool_entry( loot_pool_entry ):
        raise DatapackResourceFormatError( "LootPoolEntryFormatError" )
    output = {}

    #for key in [str(key) for key in loot_pool_entry.keys()]:

# "weight"
    dict_cp58.copy_path( output, 'weight', loot_pool_entry, 'weight' )

# "quality"
    dict_cp58.copy_path( output, 'quality', loot_pool_entry, 'quality' )

# "type"
    s = dict_cp58.get_path( loot_pool_entry, 'type' )
    #del loot_pool_entry['type']
    dict_cp58.replace_path( output, 'type', value=s )

## stash "functions"
    functions = dict_cp58.get_path( loot_pool_entry, 'functions' )
    if functions is not None:
        del loot_pool_entry['functions']

## stash "conditions"
    conditions = dict_cp58.get_path( loot_pool_entry, 'conditions' )
    if conditions is not None:
        del loot_pool_entry['conditions']

## loot_pool_entry_type
    loot_pool_entry_type = rl_cp58.namespaced( s )
# "children"
    if loot_pool_entry_type in (
        "minecraft:group",
        "minecraft:alternatives",
        "minecraft:sequence"
    ):
        loot_pool_entry_list = dict_cp58.get_path( loot_pool_entry, 'children' )
        if isinstance( loot_pool_entry_list, list ):
            dict_cp58.replace_path( output, 'children', value=list() )
            for child in loot_pool_entry_list:
                child = convert_loot_pool_entry( child )
                output['children'].append( child )
# "item"
    elif loot_pool_entry_type == "minecraft:item":
        dict_cp58.copy_path( output, 'name', loot_pool_entry, 'name' )
# "loot_table"
    elif loot_pool_entry_type == "minecraft:loot_table":
        loot_table_value = dict_cp58.get_path( loot_pool_entry, 'value' )
        if isinstance( loot_table_value, dict ):
            loot_table_value = convert_loot_table( loot_table_value )
        elif loot_table_value is not None:
            dict_cp58.replace_path( output, 'value', value=loot_table_value )
# "tag"
    elif loot_pool_entry_type == "minecraft:tag":
        item_tags_name = dict_cp58.get_path( loot_pool_entry, 'name' )
        if isinstance( item_tags_name, str ):
            dict_cp58.replace_path( output, 'items', value=f'#{item_tags_name}' )
        dict_cp58.copy_path( output, 'expand', loot_pool_entry, 'expand' )
# "dynamic"
    elif loot_pool_entry_type == "minecraft:dynamic":
        dict_cp58.copy_path( output, 'name', loot_pool_entry, 'name' )
# "slots"
    elif loot_pool_entry_type == "minecraft:slots":
        dict_cp58.copy_path( output, 'slot_source', loot_pool_entry, 'slot_source' )

# EXCEPTION
    else:
        output.update( deepcopy( loot_pool_entry ) )


# "functions" -> "modifier"
    if isinstance( functions, list ):
        functions = item_modifier.convert_loot_function( functions, allow_list=True )
        dict_cp58.replace_path( output, 'modifier', value=functions )

# "conditions" -> "condition"
    if isinstance( conditions, list ):
        conditions = predicate.convert_loot_condition( conditions )
        dict_cp58.replace_path( output, 'condition', value=conditions )
##
    return output
