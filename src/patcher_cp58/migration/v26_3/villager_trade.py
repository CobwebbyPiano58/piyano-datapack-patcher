from copy import deepcopy
from .lib import dict_cp58
from . import number_provider, predicate, item_modifier
from ...datapack import DatapackResourceFormatError

def is_villager_trade( villager_trade: dict ) -> bool:
    if isinstance( villager_trade, dict ):
        if dict_cp58.check_data_types( 
            villager_trade,
            {
                'wants': dict,
                'gives': dict
            }
        ):
            return True
    return False

def convert_villager_trade( villager_trade: dict ) -> dict:
    if not is_villager_trade( villager_trade ): 
        raise DatapackResourceFormatError( "VillagerTradeFormatError" )
    output = {}

    for key in [str(key) for key in villager_trade.keys()]:
    # "wants", "additional_wants"
        if key in (
            "wants",
            "additional_wants"
        ):
            dict_cp58.copy_path( output, ( key, 'id' ), villager_trade, ( key, 'id' ) )
            item_count = dict_cp58.get_path( villager_trade, key, 'count' )
            if item_count is not None:
                item_count = number_provider.convert_int_provider( item_count )
                dict_cp58.replace_path( output, ( key, 'count' ), value=item_count )
            dict_cp58.copy_path( output, ( key, 'components' ), villager_trade, ( key, 'components' ) )
    # "max_uses", "xp" -> context_int_provider
        elif key in (
            "max_uses",
            "xp"
        ):
            int_provider = number_provider.convert_int_provider( dict_cp58.get_path( villager_trade, key ) )
            dict_cp58.replace_path( output, key, value=int_provider )
    # "reputation_discount" -> context_float_provider
        elif key == "reputation_discount":
            float_provider = number_provider.convert_float_provider( dict_cp58.get_path( villager_trade, key ) )
            dict_cp58.replace_path( output, key, value=float_provider )
    # "given_item_modifiers" -> "given_item_modifier"
        elif key == "given_item_modifiers":
            functions = dict_cp58.get_path( villager_trade, 'given_item_modifiers' )
            if isinstance( functions, list ):
                functions = item_modifier.convert_loot_function( functions, allow_list=True )
                dict_cp58.replace_path( output, 'given_item_modifier', value=functions )
    # "merchant_predicate"
        elif key == "merchant_predicate":
            conditions = dict_cp58.get_path( villager_trade, 'merchant_predicate' )
            if isinstance( conditions, ( list, dict ) ):
                conditions = predicate.convert_predicate( conditions )
                dict_cp58.replace_path( output, 'merchant_predicate', value=conditions )
    # EXCEPTION
        else:
            output[key] = deepcopy( villager_trade[key] )
##
    return output
