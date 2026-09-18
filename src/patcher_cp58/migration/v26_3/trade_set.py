from copy import deepcopy
from .lib import dict_cp58
from . import number_provider
from ...datapack import DatapackResourceFormatError

class TradeSetFormatError( Exception ):
    pass

def is_trade_set( trade_set: dict ) -> bool:
    if isinstance( trade_set, dict ):
        if dict_cp58.check_data_types( 
            trade_set,
            {
                'trades': ( list, str ),
                'amount': ( int, float, dict )
            }
        ):
            return True
    return False

def convert_trade_set( trade_set: dict ) -> dict:
    if not is_trade_set( trade_set ): 
        raise DatapackResourceFormatError( "TradeSetFormatError" )
    output = {}

    for key in [str(key) for key in trade_set.keys()]:
    # "amount"
        if key == "amount":
            int_provider = number_provider.convert_int_provider( dict_cp58.get_path( trade_set, key ) )
            dict_cp58.replace_path( output, key, value=int_provider )
    # EXCEPTION
        else:
            output[key] = deepcopy( trade_set[key] )
##
    return output
