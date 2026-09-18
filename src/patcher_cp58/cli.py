import sys
import argparse
import traceback
from pathlib import Path

from .core import patch_datapack
from .migration import MCVersion
from .migration import get_latest_mcversion
from .migration import get_previous_mcversion
from .datapack import is_datapack

def main():
    try:
        parser = create_parser()
        if len(sys.argv) == 1:
            parser.print_help()
            return
        args = parser.parse_args()
        args = normalize_args( args )
        patch_datapack( args.input, args.source, args.target, args.output, args.format, args.name )
    except Exception:
        log_path = get_log_path()
        with log_path.open("w", encoding="utf-8") as file:
            traceback.print_exc(file=file)
        log_path.relative_to(Path.cwd())
        print(f"An unexpected error occurred.")
        print(f"ERROR LOG: {log_path}")
    finally:
        input("\nPress Enter to exit...")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Patch Minecraft Java Edition data packs between versions."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input data pack, .zip data pack, or directory containing data packs.",
    )
    parser.add_argument(
        "--target",
        help="Target Minecraft version. Defaults to the latest supported version.",
    )
    parser.add_argument(
        "--source",
        help="Source Minecraft version. Defaults to the version before target.",
    )
    parser.add_argument(
        "--format",
        choices=("zip", "folder", "overlay", "in-place"),
        default="zip",
        help="Output format. Default: zip.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory.",
    )
    parser.add_argument(
        "--name",
        help="Output data pack name.",
    )
    return parser

def normalize_args( args: argparse.Namespace ) -> argparse.Namespace:

    args.input = Path( args.input ).resolve()
    if not args.input.exists():
        raise FileNotFoundError( f'input datapach \"{args.input}\" was not found.' )
    elif not is_datapack( args.input ):
        raise ValueError( f'{args.input} is not a datapack.' )

    if args.target is None:
        args.target = get_latest_mcversion()
    else:
        args.target = MCVersion.from_name( args.target )

    if args.source is None:
        args.source = get_previous_mcversion( args.target )
    else:
        args.source = MCVersion.from_name( args.source )

    if args.format is None:
        args.format = 'zip'

    if args.output is None:
        args.output = Path( args.input ).parent

    #if args.name is None:
    #    file_name = Path( args.input ).name
    #    args.name = f'{file_name}_patched_{args.target}'

    return args

def get_log_path() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path.cwd()

    return base / "patcher_error_log.txt"
