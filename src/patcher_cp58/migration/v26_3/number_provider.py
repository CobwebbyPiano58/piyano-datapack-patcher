from copy import deepcopy
from .lib import dict_cp58, rl_cp58


def wrap_provider( provider_type: str, value: dict, provider_key='input' ) -> dict:
    output = {}
    output['type'] = provider_type
    output[provider_key] = value
    return output

def convert_int_provider( value: int | float | dict ) -> int | dict:
# is inline value
    if isinstance( value, float ):
        return int( value )
    elif not isinstance( value, dict ):
        return value
# number provider
    output = {}
    s = dict_cp58.get_path( value, 'type' )
    if s is None: 
        s = 'minecraft:uniform'
    else:
        del value['type']
    dict_cp58.replace_path( output, 'type', value=s )

    loot_number_provide_type = rl_cp58.namespaced( s )

# "binomial"
    if loot_number_provide_type == "minecraft:binomial":
        n = dict_cp58.get_path( value, 'n' )
        if n != None:
            output['n'] = convert_int_provider( n )
        p = dict_cp58.get_path( value, 'p' )
        if p != None:
            output['p'] = convert_float_provider( p )

# "constant"
    elif loot_number_provide_type == "minecraft:constant":
        dict_cp58.copy_path( output, 'value', value, 'value' )

# "enchantment_level"
    elif loot_number_provide_type == "minecraft:enchantment_level":
        output = wrap_provider( "minecraft:from_float", convert_float_provider( value ) )

# "environment_attribute"
    elif loot_number_provide_type == "minecraft:environment_attribute":
        attribute = dict_cp58.get_path( value, 'attribute' )
        if attribute != None:
            attribute = rl_cp58.namespaced( attribute )
            if attribute in (
                "minecraft:visual/fog_start_distance",
                "minecraft:visual/fog_end_distance",
                "minecraft:visual/sky_fog_end_distance",
                "minecraft:visual/cloud_fog_end_distance",
                "minecraft:visual/water_fog_start_distance",
                "minecraft:visual/water_fog_end_distance",
                "minecraft:visual/cloud_height",
                "minecraft:visual/sun_angle",
                "minecraft:visual/moon_angle",
                "minecraft:visual/star_angle",
                "minecraft:visual/star_brightness",
                "minecraft:visual/sky_light_factor",
                "minecraft:audio/music_volume",
                "minecraft:gameplay/sky_light_level",
                "minecraft:gameplay/turtle_egg_hatch_chance",
                "minecraft:gameplay/surface_slime_spawn_chance",
                "minecraft:gameplay/cat_waking_up_gift_chance",
                "minecraft:gameplay/creature_world_gen_spawn_probability"
            ):
                output = wrap_provider( "minecraft:from_float", convert_float_provider( value ) )
            else:
                dict_cp58.copy_path( output, 'attribute', value, 'attribute' )

# "score"
    elif loot_number_provide_type == "minecraft:score":
        #output.update( deepcopy( value ) )
        dict_cp58.copy_path( output, 'target', value, 'target' )
        dict_cp58.copy_path( output, 'score', value, 'score' )
        dict_cp58.copy_path( output, 'scale', value, 'scale' )

# "storage"
    elif loot_number_provide_type == "minecraft:storage":
        #output.update( deepcopy( value ) )
        dict_cp58.copy_path( output, 'storage', value, 'storage' )
        dict_cp58.copy_path( output, 'path', value, 'path' )

# "sum"
    elif loot_number_provide_type == "minecraft:sum":
        dict_cp58.replace_path( output, 'type', value='minecraft:add' )
        summands = dict_cp58.get_path( value, 'summands', default=None )
        inputs = []
        if not isinstance( summands, list ):
            summands = list()
            summands.append( int( 0 ) )
        for n in summands:
            inputs.append( convert_int_provider( n ) )
        dict_cp58.replace_path( output, 'inputs', value=inputs )

# "uniform"
    elif loot_number_provide_type == "minecraft:uniform":
        minimum = dict_cp58.get_path( value, 'min' )
        if minimum != None:
            output['min'] = convert_int_provider( minimum )
        maximum = dict_cp58.get_path( value, 'max' )
        if maximum != None:
            output['max'] = convert_int_provider( maximum )

# EXCEPTION
    else:
        output.update( deepcopy( value ) )
##
    return output


def convert_float_provider( value: int | float | dict ) -> int | dict:
# is inline value
    if isinstance( value, int ):
        return float( value )
    elif not isinstance( value, dict ):
        return value
# number provider
    output = {}
    s = dict_cp58.get_path( value, 'type' )
    if s is None: 
        s = 'minecraft:uniform'
    else:
        del value['type']
    dict_cp58.replace_path( output, 'type', value=s )

    loot_number_provide_type = rl_cp58.namespaced( s )

# "binomial"
    if loot_number_provide_type == "minecraft:binomial":
        output = wrap_provider( "minecraft:from_int", convert_int_provider( value ) )

# "constant"
    elif loot_number_provide_type == "minecraft:constant":
        dict_cp58.copy_path( output, 'value', value, 'value' )

# "enchantment_level"
    elif loot_number_provide_type == "minecraft:enchantment_level":
        output.update( deepcopy( value ) )

# "environment_attribute"
    elif loot_number_provide_type == "minecraft:environment_attribute":
        attribute = dict_cp58.get_path( value, 'attribute' )
        if attribute != None:
            attribute = rl_cp58.namespaced( attribute )
            if attribute in (
                "minecraft:visual/fog_start_distance",
                "minecraft:visual/fog_end_distance",
                "minecraft:visual/sky_fog_end_distance",
                "minecraft:visual/cloud_fog_end_distance",
                "minecraft:visual/water_fog_start_distance",
                "minecraft:visual/water_fog_end_distance",
                "minecraft:visual/cloud_height",
                "minecraft:visual/sun_angle",
                "minecraft:visual/moon_angle",
                "minecraft:visual/star_angle",
                "minecraft:visual/star_brightness",
                "minecraft:visual/sky_light_factor",
                "minecraft:audio/music_volume",
                "minecraft:gameplay/sky_light_level",
                "minecraft:gameplay/turtle_egg_hatch_chance",
                "minecraft:gameplay/surface_slime_spawn_chance",
                "minecraft:gameplay/cat_waking_up_gift_chance",
                "minecraft:gameplay/creature_world_gen_spawn_probability"
            ):
                dict_cp58.copy_path( output, 'attribute', value, 'attribute' )
            else:
                output = wrap_provider( "minecraft:from_int", convert_int_provider( value ) )

# "score"
    elif loot_number_provide_type == "minecraft:score":
        output = wrap_provider( "minecraft:from_int", convert_int_provider( value ) )

# "storage"
    elif loot_number_provide_type == "minecraft:storage":
        #output.update( deepcopy( value ) )
        dict_cp58.copy_path( output, 'storage', value, 'storage' )
        dict_cp58.copy_path( output, 'path', value, 'path' )

# "sum"
    elif loot_number_provide_type == "minecraft:sum":
        dict_cp58.replace_path( output, 'type', value='minecraft:add' )
        summands = dict_cp58.get_path( value, 'summands', default=None )
        inputs = []
        if not isinstance( summands, list ):
            summands = list()
            summands.append( int( 0 ) )
        for n in summands:
            inputs.append( convert_float_provider( n ) )
        dict_cp58.replace_path( output, 'inputs', value=inputs )

# "uniform"
    elif loot_number_provide_type == "minecraft:uniform":
        minimum = dict_cp58.get_path( value, 'min' )
        if minimum != None:
            output['min'] = convert_float_provider( minimum )
        maximum = dict_cp58.get_path( value, 'max' )
        if maximum != None:
            output['max'] = convert_float_provider( maximum )

# EXCEPTION
    else:
        output.update( deepcopy( value ) )
##
    return output


def convert_value_range( range:dict, value_type=int, can_integrate_values=True ) -> dict:
    if not isinstance( range, dict ): return value_type( range )
    output = {}
# "min"
    minimum = dict_cp58.get_path( range, 'min' )
    if minimum is not None:
        if value_type == int:
            minimum = convert_int_provider( minimum )
        elif value_type == float:
            minimum = convert_float_provider( minimum )
        output["min"] = minimum
# "max"
    maximum = dict_cp58.get_path( range, 'max' )
    if maximum is not None:
        if value_type == int:
            maximum = convert_int_provider( maximum )
        elif value_type == float:
            maximum = convert_float_provider( maximum )
        output["max"] = maximum
# integrate_values
    if can_integrate_values:
        if minimum is not None and minimum == maximum:
            output = minimum
##
    return output
