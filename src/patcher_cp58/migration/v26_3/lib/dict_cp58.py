from copy import deepcopy
from dataclasses import dataclass

@dataclass
class DataTypeItems:
    path: str | list | tuple
    value_type: str | list | tuple

def check_data_types( source_data: dict, data_type_list: list | dict ) -> bool :
    if not isinstance( source_data, dict ):
        return False
    if isinstance( data_type_list, list ):
        for data_type_items in data_type_list:
            if isinstance( data_type_items, DataTypeItems ):
                d = get_path( source_data, data_type_items.path )
                if not isinstance( d, data_type_items.value_type ):
                    return False
            elif isinstance( data_type_items, ( tuple, list ) ) and len(data_type_items)>=1:
                data_value_type = data_type_items[-1]
                del data_type_items[-1]
                d = get_path( source_data, data_type_items )
                if not isinstance( d, data_value_type ):
                    return False
        return True
    elif isinstance( data_type_list, dict ):
        for data_path in [ str(key) for key in data_type_list.keys() ]:
            d = get_path( source_data, data_path )
            if not isinstance( d, data_type_list[data_path] ):
                return False
        return True
    else:
        return False


def flatten_keys(keys):
    result = []
    for key in keys:
        if isinstance(key, (list, tuple)):
            result.extend(flatten_keys(key))
        else:
            result.append(key)
    return result

def exist_path(data, *keys):
    current = data
    keys = flatten_keys(keys)
    for key in keys:
        if not isinstance(current, dict):
            return False
        if key not in current:
            return False
        else:
            current = current[key]

    return True


def get_path(data, *keys, default=None):
    current = data
    keys = flatten_keys(keys)
    for key in keys:
        if not isinstance(current, dict):
            return default
        if key not in current:
            return default
        else:
            current = current[key]

    return current


def make_path(data, *keys, default=None):
    if default == None : default = {}
    current = data
    keys = flatten_keys(keys)
    i = len(keys)
    for key in keys:
        i -= 1
        if not isinstance(current, dict):
            return
        if key not in current:
            if i == 0 : 
                current[key] = deepcopy(default)
            else:
                current[key] = {}
        current = current[key]

def get_child(current, key):
    if isinstance(current, dict):
        if key not in current:
            current[key] = {}
        return current.get(key)
    if isinstance(current, list) and isinstance(key, int):
        if 0 <= key < len(current):
            return current[key]
    return None

def replace_path(data, *keys, value=None):
    if value is None:
        value = {}
    keys = flatten_keys(keys)
    if not keys:
        return
    current = data
    for key in keys[:-1]:
        current = get_child(current, key)
        if current is None:
            return
    last_key = keys[-1]
    if isinstance(current, dict):
        current[last_key] = deepcopy(value)
    elif isinstance(current, list) and isinstance(last_key, int):
        if not (0 <= last_key < len(current)):
            return
        current[last_key] = deepcopy(value)

def merge_path(data, *keys, value=None):
    if value is None:
        value = {}
    keys = flatten_keys(keys)
    if not keys:
        return
    current = data
    for key in keys[:-1]:
        current = get_child(current, key)
        if current is None:
            return
    last_key = keys[-1]
    if isinstance(current, dict):
        if isinstance(value, dict):
            if last_key not in current:
                current[last_key] = {}
            if not isinstance(current[last_key], dict):
                current[last_key] = {}
            current[last_key].update(deepcopy(value))
        else:
            current[last_key] = deepcopy(value)
    elif isinstance(current, list) and isinstance(last_key, int):
        if not (0 <= last_key < len(current)):
            return
        if isinstance(value, dict):
            if not isinstance(current[last_key], dict):
                return
            current[last_key].update(deepcopy(value))
        else:
            current[last_key] = deepcopy(value)

def copy_path( target_data, target_path, source_data, source_path, default=None ):

    value = get_path( source_data, source_path )
    if value is None :
        if default is None:
            return
        else :
            value = default

    replace_path( target_data, target_path, value= value )

