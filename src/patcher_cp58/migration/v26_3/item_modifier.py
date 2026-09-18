from copy import deepcopy
from .lib import dict_cp58, rl_cp58
from . import number_provider, predicate, loot_table
from ...datapack import DatapackResourceFormatError

def is_loot_function( modifier: dict | list ) -> bool:
    if isinstance( modifier, dict ):
        s = dict_cp58.get_path( modifier, 'function' )
        if isinstance( s, str ): return True
    elif isinstance( modifier, list ):
        return True
    return False

def wrap_loot_function( functions: list | dict | str ) -> dict:
    output = {
        "type": "minecraft:sequence",
        "functions": []
    }
    if isinstance( functions, list ):
        l = len(functions)
        if l <= 0:
            dict_cp58.replace_path( output, 'functions', value=[] )
        elif l == 1:
            #modifier = convert_item_modifier( functions[0] )
            #dict_cp58.replace_path( output, 'functions', value=modifier )
            return convert_loot_function( functions[0] )
        else:
            modifier_list = list()
            for f in functions:
                modifier_list.append( convert_loot_function( f ) )
            dict_cp58.replace_path( output, 'functions', value=modifier_list )
            #return modifier_list
    elif isinstance( functions, dict ):
        return convert_loot_function( functions )
    else:
    #elif isinstance( functions, str ):
        dict_cp58.replace_path( output, 'functions', value=functions )
    return output


def convert_item_modifier( modifier: dict | list ) -> dict:
    if isinstance( modifier, list ):
        modifier = wrap_loot_function( modifier )
    else:
        modifier = convert_loot_function( modifier )
        if isinstance( modifier, str ):
            modifier = wrap_loot_function( modifier )
    return modifier


def convert_loot_function( modifier: dict | list, allow_list: bool = None ) -> ( dict | list ):
    if not is_loot_function( modifier ): 
        raise DatapackResourceFormatError( "ItemModifierFormatError" )
    if isinstance( modifier, list ):
        if allow_list is None : allow_list = False
        if allow_list :
            sequence_list = []
            for f in modifier:
                sequence_list.append( convert_loot_function( f ) )
            return sequence_list
        else:
            return wrap_loot_function( modifier )

    output = {}
## "function" -> "type"
    s = dict_cp58.get_path( modifier, 'function' )
    dict_cp58.replace_path( output, 'type', value=s )
    del modifier['function']

## stash "conditions"
    conditions = dict_cp58.get_path( modifier, 'conditions' )
    if conditions is not None:
        del modifier['conditions']

## loot_function_type
    loot_function_type = rl_cp58.namespaced( s )

# no changes
    if loot_function_type in (
        "minecraft:apply_bonus",
        "minecraft:copy_components",
        "minecraft:copy_custom_data",
        "minecraft:copy_name",
        "minecraft:copy_state",
        "minecraft:enchant_randomly",
        "minecraft:exploration_map",
        "minecraft:fill_player_head",
        "minecraft:furnace_smelt",
        "minecraft:set_banner_pattern",
        "minecraft:set_book_cover",
        "minecraft:set_components",
        "minecraft:set_custom_data",
        "minecraft:set_firework_explosion",
        "minecraft:set_fireworks",
        "minecraft:set_instrument",
        "minecraft:set_item",
        "minecraft:set_lore",
        "minecraft:set_name",
        "minecraft:set_potion",
        "minecraft:set_random_potion",
        "minecraft:set_writable_book_pages",
        "minecraft:set_written_book_pages",
        "minecraft:toggle_tooltips"
    ):
        output.update( deepcopy( modifier ) )

# empty
    elif loot_function_type in (
        "minecraft:discard"
        "minecraft:explosion_decay"
    ):
        pass

# "enchant_with_levels"
    elif loot_function_type == "minecraft:enchant_with_levels":
        levels = dict_cp58.get_path( modifier, 'levels' )
        if levels is not None:
            levels = number_provider.convert_int_provider( levels )
            dict_cp58.replace_path( output, 'levels', value=levels )
        dict_cp58.copy_path( output, 'options', modifier, 'options' )
        dict_cp58.copy_path( output, 'include_additional_cost_component', modifier, 'include_additional_cost_component' )

# "enchanted_count_increase"
    elif loot_function_type == "minecraft:enchanted_count_increase":
        dict_cp58.copy_path( output, 'enchantment', modifier, 'enchantment' )
        count = dict_cp58.get_path( modifier, 'count' )
        if count is not None:
            count = number_provider.convert_int_provider( count )
            dict_cp58.replace_path( output, 'count', value=count )
        dict_cp58.copy_path( output, 'limit', modifier, 'limit' )

# "filtered"
    elif loot_function_type == "minecraft:filtered":
        dict_cp58.copy_path( output, 'item_filter', modifier, 'item_filter' )
        on_pass = dict_cp58.get_path( modifier, 'on_pass' )
        if on_pass is not None:
            on_pass = convert_loot_function( on_pass )
            dict_cp58.replace_path( output, 'on_pass', value=on_pass )
        on_fail = dict_cp58.get_path( modifier, 'on_fail' )
        if on_fail is not None:
            on_fail = convert_loot_function( on_fail )
            dict_cp58.replace_path( output, 'on_fail', value=on_fail )

# "limit_count"
    elif loot_function_type == "minecraft:limit_count":
        limit = dict_cp58.get_path( modifier, 'limit' )
        if isinstance( limit, dict ):
            limit = number_provider.convert_value_range( limit, can_integrate_values=False )
        else:
            limit = number_provider.convert_int_provider( limit )
            d = { "min": 0, "max": 0 }
            d["min"] = limit
            d["max"] = limit
            limit = d
        dict_cp58.replace_path( output, 'limit', value=limit )

# "modify_contents"
    elif loot_function_type == "minecraft:modify_contents":
        dict_cp58.copy_path( output, 'component', modifier, 'component' )
        contents_modifier = dict_cp58.get_path( modifier, 'modifier' )
        if contents_modifier is not None:
            contents_modifier = convert_loot_function( contents_modifier )
            dict_cp58.replace_path( output, 'modifier', value=contents_modifier )


# "reference"
    elif loot_function_type == "minecraft:reference":
        item_modifier_id = dict_cp58.get_path( modifier, 'name' )
        if item_modifier_id is not None:
            if conditions is None:
                output = item_modifier_id
            else:
                output.update( wrap_loot_function( item_modifier_id ) )

# "sequence"
    elif loot_function_type == "minecraft:sequence":
        functions = dict_cp58.get_path( modifier, 'functions' )
        if isinstance( functions, list ):
            l = len(functions)
            if l <= 0:
                dict_cp58.replace_path( output, 'functions', value=[] )
            elif l == 1:
                modifier_element = convert_loot_function( functions[0] )
                dict_cp58.replace_path( output, 'functions', value=modifier_element )
            else:
                modifier_list = list()
                for f in functions:
                    modifier_list.append( convert_loot_function( f ) )
                dict_cp58.replace_path( output, 'functions', value=modifier_list )

# "set_attributes"
    elif loot_function_type == "minecraft:set_attributes":
        attribute_modifiers = dict_cp58.get_path( modifier, 'modifiers' )
        if isinstance( attribute_modifiers, list ):
            modifier_list = list()
            for modifier_element in attribute_modifiers:
                if not isinstance( modifier_element, dict ): continue
                modifier_list.append( dict() )
                dict_cp58.copy_path( modifier_list[-1], 'id', modifier_element, 'id' )
                dict_cp58.copy_path( modifier_list[-1], 'attribute', modifier_element, 'attribute' )
                dict_cp58.copy_path( modifier_list[-1], 'operation', modifier_element, 'operation' )
                amount = dict_cp58.get_path( modifier_element, 'amount' )
                if amount is not None:
                    amount = number_provider.convert_float_provider( amount )
                    dict_cp58.replace_path( modifier_list[-1], 'amount', value=amount )
                dict_cp58.copy_path( modifier_list[-1], 'slot', modifier_element, 'slot' )
            dict_cp58.replace_path( output, 'modifiers', value=modifier_list )

# "set_contents"
    elif loot_function_type == "minecraft:set_contents":
        dict_cp58.copy_path( output, 'component', modifier, 'component' )
        entries = dict_cp58.get_path( modifier, 'entries' )
        if isinstance( entries, list ):
            loot_entry_list = list()
            for loot_entry in entries:
                loot_entry_list.append( loot_table.convert_loot_pool_entry( loot_entry ) )
            dict_cp58.replace_path( output, 'entries', value=loot_entry_list )

# "set_count"
    elif loot_function_type == "minecraft:set_count":
        count = dict_cp58.get_path( modifier, 'count' )
        if count is not None:
            count = number_provider.convert_int_provider( count )
            dict_cp58.replace_path( output, 'count', value=count )
        dict_cp58.copy_path( output, 'add', modifier, 'add' )

# "set_custom_model_data"
    elif loot_function_type == "minecraft:set_custom_model_data":
    # floats
        list_modifier = dict_cp58.get_path( modifier, 'floats' )
        if list_modifier is not None:
            values = dict_cp58.get_path( list_modifier, 'values' )
            if isinstance( values, list ):
                float_provider_list = list()
                for np in values:
                    float_provider_list.append( number_provider.convert_float_provider( np ) )
                dict_cp58.replace_path( list_modifier, 'values', value=float_provider_list )
            dict_cp58.replace_path( output, 'floats', value=list_modifier )
    # flags
        dict_cp58.copy_path( output, 'flags', modifier, 'flags' )
    # strings
        dict_cp58.copy_path( output, 'strings', modifier, 'strings' )
    # colors
        list_modifier = dict_cp58.get_path( modifier, 'colors' )
        if list_modifier is not None:
            values = dict_cp58.get_path( list_modifier, 'values' )
            if isinstance( values, list ):
                color_list = list()
                for color_value in values:
                    if isinstance( color_value, list ):
                        color_list.append( color_value )
                    else:
                        color_list.append( number_provider.convert_int_provider( color_value ) )
                dict_cp58.replace_path( list_modifier, 'values', value=color_list )
            dict_cp58.replace_path( output, 'colors', value=list_modifier )

# "set_damage"
    elif loot_function_type == "minecraft:set_damage":
        damage = dict_cp58.get_path( modifier, 'damage' )
        if damage is not None:
            damage = number_provider.convert_float_provider( damage )
            dict_cp58.replace_path( output, 'damage', value=damage )
        dict_cp58.copy_path( output, 'add', modifier, 'add' )

# "set_enchantments"
    elif loot_function_type == "minecraft:set_enchantments":
        enchantments = dict_cp58.get_path( modifier, 'enchantments' )
        if isinstance( enchantments, dict ):
            for enchant_id, enchant_level in enchantments.items():
                enchant_level = number_provider.convert_int_provider( enchant_level )
                dict_cp58.replace_path( output, 'enchantments',enchant_id, value=enchant_level )
        dict_cp58.copy_path( output, 'add', modifier, 'add' )

# "set_loot_table"
    elif loot_function_type == "minecraft:set_loot_table":
        dict_cp58.copy_path( output, 'loot_table_id', modifier, 'name' )
        #dict_cp58.copy_path( output, 'loot_table_id', function, 'tag' )
        dict_cp58.copy_path( output, 'seed', modifier, 'seed' )

# # "set_ominous_bottle_amplifier"
    elif loot_function_type == "minecraft:set_ominous_bottle_amplifier":
        amplifier = dict_cp58.get_path( modifier, 'amplifier' )
        if amplifier is not None:
            amplifier = number_provider.convert_int_provider( amplifier )
            dict_cp58.replace_path( output, 'amplifier', value=amplifier )

# # "set_random_dyes"
    elif loot_function_type == "minecraft:set_random_dyes":
        count = dict_cp58.get_path( modifier, 'number_of_dyes' )
        if count is not None:
            count = number_provider.convert_int_provider( count )
            dict_cp58.replace_path( output, 'number_of_dyes', value=count )

# "set_stew_effect"
    elif loot_function_type == "minecraft:set_stew_effect":
        stew_effects = dict_cp58.get_path( modifier, 'effects' )
        if isinstance( stew_effects, list ):
            effect_list = list()
            for effect in stew_effects:
                effect_list.append( dict() )
                dict_cp58.copy_path( effect_list[-1], 'type', effect, 'type' )
                effect_duration = dict_cp58.get_path( effect, 'duration' )
                if effect_duration is not None:
                    effect_duration = number_provider.convert_int_provider( effect_duration )
            dict_cp58.replace_path( output, 'effects', value=effect_list )

# EXCEPTION
    else:
        output.update( deepcopy( modifier ) )

## "conditions" -> "condition"
    if conditions is not None:
        condition = predicate.convert_loot_condition( conditions )
        dict_cp58.replace_path( output, 'condition', value=condition )
##
    return output
