from pathlib import Path
from dataclasses import dataclass, field
import shutil
import tempfile
from json import JSONDecodeError
from .datapack import DatapackResource
from .datapack import DatapackResourceFormatError

from . import migration

@dataclass
class DatapackPatchResult():
    success_data: dict = field(default_factory=dict)
    fail_data: dict = field(default_factory=dict)

    def save_result( self, path:Path ):
        path = Path( path ).resolve()
        log = []

        counts = {}
        for data_type in [str(key) for key in self.success_data.keys()]:
            log.append( self.log_output( f'{data_type}' ) )
            i = 0
            for rl in [str(key) for key in self.success_data[data_type].keys()]:
                log.append( self.log_output( f'  {rl}' ) )
                i += 1
            counts[data_type] = i
            log.append( self.log_output( '' ) )
        log.append( self.log_output('TOTAL:') )
        for data_type, i in counts.items():
            log.append( self.log_output(f'  {data_type}: {i}') )

        with path.open("w", encoding="utf-8") as file:
            file.writelines( log )

    def log_output( self, text:str ):
        text = str( text )
        print( text )
        return text + '\n'

    def add_success( self, data_type:str, rl:str ):
        self.success_data.setdefault( data_type, {} )[rl] = {}

    def add_fail( self, data_type:str, rl:str, error=None ):
        self.fail_data.setdefault( data_type, {} )[rl] = {}
        if error is not None:
            self.fail_data[data_type][rl]['error'] = error

    @property
    def success( self ) -> int:
        i = 0
        for data_type in [str(key) for key in self.success_data.keys()]:
            i += len( self.success_data[data_type] )
        return i

    @property
    def fail( self ) -> int:
        i = 0
        for data_type in [str(key) for key in self.fail_data.keys()]:
            i += len( self.fail_data[data_type] )
        return i

###################################################################################

def patch_datapack( datapack_path: Path, source_version=None, target_version=None, output_path=None, output_mode=None, output_name=None ):
    if not datapack_path.is_dir():
        raise FileNotFoundError()
    if output_path is None:
        output_path = Path( datapack_path ).parent
    if output_mode is None:
        output_mode = 'zip'

    target_version = migration.get_version_from_name( target_version )

    converters = migration.get_converters( source_version, target_version )

    datapack_output = Path()
    if output_mode == 'in-place':
        datapack_output = datapack_path
    else:
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = Path( temp_dir.name )
        ( temp_path / 'data' ).mkdir( exist_ok=True )
        if output_mode == 'overlay':
            shutil.copy2( 
                datapack_path / "pack.mcmeta",
                temp_path
            )
        else:
            shutil.copytree( 
                datapack_path, 
                temp_path, 
                ignore= ignore_dirs,
                dirs_exist_ok=True
            )
        datapack_output = temp_path

    patch_result = DatapackPatchResult()

    data_path = datapack_path / 'data'
    for namespace_path in data_path.iterdir():
        if not namespace_path.is_dir(): continue
        namespace = namespace_path.name
        for data_type in [str(key) for key in converters.keys()]:
            type_path = namespace_path / data_type
            if not type_path.exists(): continue
            for json_path in type_path.rglob("*.json"):
                try:
                    datapack_resource = DatapackResource( datapack_path, data_type, namespace, json_path )
                except ( JSONDecodeError, UnicodeDecodeError ) as error:
                    pass
                else:
                    try:
                        for converter in converters[data_type]:
                            datapack_resource.data = converter( datapack_resource.data )
                    except DatapackResourceFormatError as error:
                        print( f'[ DatapackResourceFormatError {error.args[0]} {datapack_resource.data_type} {datapack_resource.rl} ]' )
                        patch_result.add_fail( data_type, datapack_resource.rl, error.args[0] )
                    else:
                        datapack_resource.save_data( datapack_output )
                        patch_result.add_success( data_type, datapack_resource.rl )

    patch_result.save_result( ( datapack_output / 'patch_log.txt' ) )

    if output_mode == 'in-place':
        pass
    else:
        if output_name is None:
            output_name = f'{datapack_path.name}_patched_{target_version}'
        if output_mode == 'zip':
            shutil.make_archive( output_path / output_name, format='zip', root_dir=temp_path )
        elif output_mode == 'folder':
            shutil.copytree( temp_path, output_path / output_name , dirs_exist_ok=True )
        elif output_mode == 'overlay':
            shutil.copytree( temp_path, output_path / output_name , dirs_exist_ok=True )
        temp_dir.cleanup()

###################################################################################

def ignore_dirs(path, names):
    path = Path(path)
    return [
        name
        for name in names
        if (
            ( (path / name).is_dir() and name.startswith(".") ) 
            or 
            ( (path / name).is_file() and name.endswith(".zip") )
        )
    ]
        