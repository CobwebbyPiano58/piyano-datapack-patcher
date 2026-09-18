from dataclasses import dataclass, field
from pathlib import Path
import json
from zipfile import ZipFile, is_zipfile

@dataclass
class DatapackResource:
    datapack: Path
    data_type: str
    namespace: str
    path: Path
    data: dict | list = field(init=False)

    @property
    def rl( self ):
        p = self.path.with_suffix("").as_posix()
        return f"{self.namespace}:{p}"

    def __post_init__(self):
        self.path = self.path.relative_to( ( self.datapack / "data" / self.namespace / self.data_type ) )
        self.load_data()

    def file_path( self, datapach_path: Path ):
        return Path( datapach_path / "data" / self.namespace / self.data_type / self.path )

    def load_data( self ):
        file_path = self.file_path( self.datapack )
        try:
            with file_path.open("r", encoding="utf-8") as f:
                if file_path.suffix == '.json' :
                    self.data = json.load(f)
                else:
                    self.data = f.read()
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise error

    def save_data( self, datapach_path: Path ):
        path = self.file_path( datapach_path )
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)


class DatapackResourceFormatError( Exception ):
    pass


def is_datapack( path:Path, allow_zip:bool=None ) -> bool:
    path = Path(path).resolve()
    if (
        path.is_dir()
        and path != Path(path.anchor)
        and (path / "data").is_dir()
    ):
        mcmeta = json.loads((path / "pack.mcmeta").read_text(encoding="utf-8"))
        if 'pack' in mcmeta :
            return True
    elif (
        allow_zip is True,
        path.is_file()
        and is_zipfile(path)
    ):
        with ZipFile(path) as zf:
            names = zf.namelist()
            if not any(name.startswith("data/") for name in names):
                return False
            if "pack.mcmeta" not in names:
                return False
            try:
                with zf.open("pack.mcmeta") as file:
                    mcmeta = json.load(file)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return False
            return isinstance(mcmeta.get("pack"), dict)
    return False
