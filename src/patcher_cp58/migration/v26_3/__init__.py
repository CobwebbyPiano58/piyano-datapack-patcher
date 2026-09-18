from .advancement import convert_advancement
from .enchantment import convert_enchantment
from .item_modifier import convert_item_modifier
from .loot_table import convert_loot_table
from .predicate import convert_predicate
from .trade_set import convert_trade_set
from .villager_trade import convert_villager_trade

CONVERTERS = {
    "advancement": convert_advancement,
    "enchantment": convert_enchantment,
    "item_modifier": convert_item_modifier,
    "loot_table": convert_loot_table,
    "predicate": convert_predicate,
    "trade_set": convert_trade_set,
    "villager_trade": convert_villager_trade
}
