from copy import deepcopy
from .lib import dict_cp58, rl_cp58
from . import predicate
from ...datapack import DatapackResourceFormatError

def is_enchantment( enchant: dict ) -> bool:
    if isinstance( enchant, dict ):
        if dict_cp58.check_data_types( 
            enchant,
            {
                'anvil_cost': ( int, float ),
                'description': ( str, dict ),
                'max_cost': dict,
                'max_level': ( int, float ),
                'min_cost': dict,
                'slots': list,
                'supported_items': ( list, str ),
                'weight': ( int, float )
            }
        ):
            return True
    return False

def convert_enchantment( enchant: dict ) -> dict:
    if not is_enchantment( enchant ): 
        raise DatapackResourceFormatError( "EnchantmentFormatError" )

    output = {}
    output.update( deepcopy( enchant ) )
    for key in [ str(key) for key in enchant.keys() ]:
        if key == "effects":
            output['effects'] = dict()
            for s in [ str(key) for key in enchant['effects'].keys() ]:
                #effect_component_type = rl_cp58.namespaced( s )
                effect_component_list = enchant['effects'][s]
                if isinstance( effect_component_list, list ):
                    output['effects'][s] = list()
                    for effect_component in effect_component_list:
                        if dict_cp58.check_data_types( effect_component, { 'effect': dict, 'requirements': dict } ):
                            requirements = predicate.convert_loot_condition( effect_component['requirements'] )
                            del effect_component['requirements']
                            output['effects'][s].append( deepcopy( effect_component ) )
                            output['effects'][s][-1]['requirements'] = requirements
                        else:
                            output['effects'][s].append( deepcopy( effect_component ) )
                else:
                    output['effects'][s] = deepcopy( effect_component_list )
        else:
            output[key] = deepcopy( enchant[key] )
##
    return output
