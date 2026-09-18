from dataclasses import dataclass
from . import v26_3

VERSIONS = {
    "26.2": None,
    "26.3": v26_3
}


@dataclass(frozen=True)
class MCVersion():
    name: str
    data_version: int
    datapack_format: int
    resourcepack_format: int

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"MCVersion(name={self.name!r})"

    @classmethod
    def from_name( cls, name: str ):
        for v in DATAVERSIONS:
            if v.name == name:
                return v
        raise ValueError( f'Unknown version: {name}' )

    @classmethod
    def from_data_version( cls, data_version: int ):
        f = -1.0
        for v in DATAVERSIONS:
            if data_version > v.data_version:
                if f is not None:
                    if f > data_version:
                        return v
                else:
                    return v
            elif v.data_version == data_version:
                return v
            f = v.data_version
        raise ValueError( f'Unknown data version: {data_version}' )

    @classmethod
    def from_datapack_format( cls, datapack_format: float ):
        f = -1.0
        for v in DATAVERSIONS:
            if datapack_format > v.datapack_format:
                if f is not None:
                    if f > datapack_format:
                        return v
            elif v.datapack_format == datapack_format:
                return v
            f = v.datapack_format
        raise ValueError( f'Unknown datapack format: {datapack_format}' )

    @classmethod
    def from_resourcepack_format( cls, resourcepack_format: float ):
        f = -1.0
        for v in DATAVERSIONS:
            if resourcepack_format > v.resourcepack_format:
                if f is not None:
                    if f > resourcepack_format:
                        return v
            elif v.resourcepack_format == resourcepack_format:
                return v
            f = v.resourcepack_format
        raise ValueError( f'Unknown resourcepack format: {resourcepack_format}' )


DATAVERSIONS = [
    MCVersion(
        name="26.3", 
        data_version=5023, 
        datapack_format=120.0, 
        resourcepack_format=97.1
    ),
    MCVersion(
        name="26.2",
        data_version=4903,
        datapack_format=107.1,
        resourcepack_format=88.0
    )
]

def get_converters( source_version:str=None, target_version:str=None ) -> dict:
    output = {}
    try:
        for migration in get_migrations(source_version, target_version):
            for data_type, converter in migration.CONVERTERS.items():
                output.setdefault(data_type, []).append(converter)
    except ValueError as error:
        print( error )
        raise
##
    return output

def get_migrations( source_version:str=None, target_version:str=None ):
    
    version_list = [ str(key) for key in VERSIONS.keys() ]

    target_version = get_version_from_name( target_version )
    target_index = version_list.index( str( target_version ) )

    source_version = get_version_from_name( source_version, default=version_list[target_index-1] )
    source_index = version_list.index( str( source_version ) )

    if source_index >= target_index:
        raise ValueError( f"Invalid migration range: {source_version} -> {target_version}" )

    migrations = version_list[ source_index+1 : target_index+1 ]
    #print( f'{source_version} -> {target_version}  =  {migrations}' )

    return [ VERSIONS[version] for version in migrations ]

def get_version_from_name( version:str, default=None ) -> str:
    if version is None :
        if default is None:
            version = next(iter(reversed(VERSIONS)))
        else:
            version = default
    elif isinstance( version, str ) :
        if version in VERSIONS:
            pass
        else:
            raise ValueError( f'Invalid version: {version}' )
    elif isinstance( version, MCVersion ):
        if version.name in VERSIONS:
            pass
        else:
            raise ValueError( f'Invalid version: {version}' )
    else:
        raise TypeError( )
    return version


def get_latest_mcversion(  ) -> MCVersion:
    return DATAVERSIONS[0]

def get_previous_mcversion( input_mcv:MCVersion ) -> MCVersion:
    data_version = input_mcv.data_version
    f = None
    for i, v in enumerate( DATAVERSIONS ):
        if data_version > v.data_version:
            if f is not None:
                if f > data_version:
                    return v
            else:
                return v
        elif v.data_version == data_version:
            i += 1
            if len( DATAVERSIONS ) > i:
                return DATAVERSIONS[i]
        f = v.data_version
    raise IndexError( "There's no previous mcversion." )
