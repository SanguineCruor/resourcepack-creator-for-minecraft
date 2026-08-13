#!/usr/bin/env python3
"""Simple Minecraft resource pack builder.

Usage:
    python resourcepack_builder.py init my_pack
    python resourcepack_builder.py build my_pack -o my_pack.zip
    python resourcepack_builder.py validate my_pack
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

DEFAULT_PACK_FORMAT = 12
DEFAULT_MC_VERSION = "1.20 - 1.20.1"
DEFAULT_DESCRIPTION = "Minecraft resource pack"
DEFAULT_AUTHOR = "Unknown"

PACK_FORMAT_REFERENCE = [
    {"version": "1.6.1 - 1.8.9", "kind": "pack_format", "value": 1},
    {"version": "1.9 - 1.10.2", "kind": "pack_format", "value": 2},
    {"version": "1.11 - 1.12.2", "kind": "pack_format", "value": 3},
    {"version": "1.13 - 1.14.4", "kind": "pack_format", "value": 4},
    {"version": "1.15 - 1.16.1", "kind": "pack_format", "value": 5},
    {"version": "1.16.2 - 1.16.5", "kind": "pack_format", "value": 6},
    {"version": "1.17 - 1.17.1", "kind": "pack_format", "value": 7},
    {"version": "1.18 - 1.18.2", "kind": "pack_format", "value": 8},
    {"version": "1.19 - 1.19.2", "kind": "pack_format", "value": 9},
    {"version": "1.19.3", "kind": "pack_format", "value": 10},
    {"version": "1.19.4", "kind": "pack_format", "value": 12},
    {"version": "1.20 - 1.20.1", "kind": "pack_format", "value": 15},
    {"version": "1.20.2", "kind": "pack_format", "value": 18},
    {"version": "1.20.3 - 1.20.4", "kind": "pack_format", "value": 26},
    {"version": "1.20.5 - 1.20.6", "kind": "pack_format", "value": 32},
    {"version": "1.21 - 1.21.1", "kind": "pack_format", "value": 34},
    {"version": "1.21.2 - 1.21.3", "kind": "pack_format", "value": 42},
    {"version": "1.21.4", "kind": "pack_format", "value": 46},
    {"version": "1.21.5", "kind": "pack_format", "value": 55},
    {"version": "1.21.6", "kind": "pack_format", "value": 63},
    {"version": "1.21.7 - 1.21.8", "kind": "pack_format", "value": 64},
    {"version": "1.21.9 - 1.21.10", "kind": "minmax", "min_format": 88.0, "max_format": 88.0},
    {"version": "1.21.11", "kind": "minmax", "min_format": 94.1, "max_format": 94.1},
]


def make_pack_mcmeta(name: str, description: str, pack_format: int | float | None, author: str, min_format: float | None = None, max_format: float | None = None) -> dict:
    pack_data = {
        "description": description,
    }
    if min_format is not None and max_format is not None:
        pack_data["min_format"] = min_format
        pack_data["max_format"] = max_format
    else:
        pack_data["pack_format"] = pack_format if pack_format is not None else DEFAULT_PACK_FORMAT
    return {
        "pack": pack_data,
        "author": author,
    }


def write_pack_mcmeta(path: Path, name: str, description: str, pack_format: int | float | None, author: str, min_format: float | None = None, max_format: float | None = None) -> None:
    data = make_pack_mcmeta(name, description, pack_format, author, min_format=min_format, max_format=max_format)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def validate_resourcepack_folder(folder: Path) -> list[str]:
    errors: list[str] = []
    if not folder.exists() or not folder.is_dir():
        errors.append(f"Resource pack folder does not exist: {folder}")
        return errors

    pack_mcmeta = folder / "pack.mcmeta"
    if not pack_mcmeta.exists():
        errors.append("Missing pack.mcmeta")
    else:
        try:
            with pack_mcmeta.open("r", encoding="utf-8") as file:
                content = json.load(file)
            if "pack" not in content:
                errors.append("pack.mcmeta is invalid: missing pack section")
            elif "pack_format" in content["pack"]:
                pass
            elif "min_format" in content["pack"] and "max_format" in content["pack"]:
                pass
            else:
                errors.append("pack.mcmeta is invalid or missing pack_format/min_format/max_format")
        except json.JSONDecodeError:
            errors.append("pack.mcmeta contains invalid JSON")

    if not any(folder.glob("**/assets/minecraft/**/*")):
        errors.append("No assets/minecraft folder structure found")
    return errors


def build_zip(source: Path, output: Path, icon: Path | None = None, name: str | None = None, description: str | None = None, author: str | None = None, pack_format: int | float | None = None, min_format: float | None = None, max_format: float | None = None) -> None:
    source = source.resolve()
    output = output.resolve()

    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"Source folder not found: {source}")

    pack_mcmeta_path = source / "pack.mcmeta"
    if not pack_mcmeta_path.exists():
        if not name:
            name = source.name
        if description is None:
            description = DEFAULT_DESCRIPTION
        if author is None:
            author = DEFAULT_AUTHOR
        if pack_format is None:
            pack_format = DEFAULT_PACK_FORMAT
        print(f"Generating pack.mcmeta for '{source.name}'")
        write_pack_mcmeta(pack_mcmeta_path, name, description, pack_format, author, min_format=min_format, max_format=max_format)

    if icon:
        icon = icon.resolve()
        if not icon.exists():
            raise FileNotFoundError(f"Icon file not found: {icon}")

    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for file_path in sorted(source.rglob("*")):
            if file_path.is_file():
                relative_path = file_path.relative_to(source)
                archive.write(file_path, relative_path.as_posix())

        if icon:
            archive.write(icon, "pack.png")

    print(f"Created resource pack: {output}")


def create_template(folder: Path, name: str, description: str, author: str, pack_format: int | float | None, min_format: float | None = None, max_format: float | None = None) -> None:
    # resolve to absolute path to avoid confusion where files are created
    folder = folder.expanduser()
    try:
        folder = folder.resolve()
    except Exception:
        # resolve may fail on non-existing paths on some systems, continue with expanduser result
        pass

    if folder.exists():
        if not folder.is_dir():
            raise FileExistsError(f"Path exists and is not a folder: {folder}")
    else:
        folder.mkdir(parents=True, exist_ok=True)

    assets_dir = folder / "assets" / "minecraft" / "textures"
    assets_dir.mkdir(parents=True, exist_ok=True)

    pack_mcmeta = folder / "pack.mcmeta"
    already_exists = pack_mcmeta.exists()
    write_pack_mcmeta(pack_mcmeta, name, description, pack_format, author, min_format=min_format, max_format=max_format)
    if already_exists:
        print(f"Updated {pack_mcmeta}")
    else:
        print(f"Created {pack_mcmeta}")

    icon_file = folder / "pack.png"
    if not icon_file.exists():
        icon_file.write_bytes(b"")
        print(f"Created placeholder icon: {icon_file}")
    else:
        print(f"Icon already exists: {icon_file}")

    print(f"Template folder created at {folder}")


def resolve_version_entry(selection: str | None) -> dict:
    if selection is None or selection.strip() == "":
        selection = DEFAULT_MC_VERSION

    normalized = selection.strip().lower()
    if normalized.isdigit():
        index = int(normalized)
        if 1 <= index <= len(PACK_FORMAT_REFERENCE):
            return PACK_FORMAT_REFERENCE[index - 1]

    for entry in PACK_FORMAT_REFERENCE:
        if normalized == entry["version"].lower():
            return entry

    raise ValueError(f"Version not recognized: {selection}")


def prompt_version_selection(default_version: str | None = None) -> dict:
    print("Выберите версию Minecraft / Choose Minecraft version:")
    for index, entry in enumerate(PACK_FORMAT_REFERENCE, start=1):
        if entry["kind"] == "pack_format":
            print(f"  {index}. {entry['version']} -> pack_format = {entry['value']}")
        else:
            print(f"  {index}. {entry['version']} -> min_format = {entry['min_format']}, max_format = {entry['max_format']}")

    default_value = default_version or DEFAULT_MC_VERSION
    choice = ask_input("Введите номер или точное название версии / Enter a number or exact version name", default_value)
    return resolve_version_entry(choice)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Minecraft resource pack builder",
        epilog=(
            "Examples:\n"
            "  python resourcepack_builder.py init my_pack\n"
            "  python resourcepack_builder.py build my_pack -o my_pack.zip\n"
            "  python resourcepack_builder.py validate my_pack\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    init_parser = subparsers.add_parser("init", help="Create a starter resource pack folder")
    init_parser.add_argument("folder", type=Path, nargs="?", help="Target folder for the starter pack")
    init_parser.add_argument("--name", default="My Resource Pack", help="Resource pack name")
    init_parser.add_argument("--description", default=DEFAULT_DESCRIPTION, help="Pack description")
    init_parser.add_argument("--author", default=DEFAULT_AUTHOR, help="Pack author")
    init_parser.add_argument("--version", help="Minecraft version to target (for example 1.21.11 or 1.20 - 1.20.1)")
    init_parser.add_argument("--pack-format", type=int, default=None, help="Manual Minecraft pack_format number")

    build_parser = subparsers.add_parser("build", help="Build a ZIP from a resource pack folder")
    build_parser.add_argument("source", type=Path, help="Source resource pack folder")
    build_parser.add_argument("-o", "--output", type=Path, default=Path("resourcepack.zip"), help="Output ZIP file")
    build_parser.add_argument("--icon", type=Path, help="Optional pack icon file (pack.png)")
    build_parser.add_argument("--name", help="Pack name when generating pack.mcmeta")
    build_parser.add_argument("--description", help="Pack description when generating pack.mcmeta")
    build_parser.add_argument("--author", help="Pack author")
    build_parser.add_argument("--version", help="Minecraft version to target (for example 1.21.11 or 1.20 - 1.20.1)")
    build_parser.add_argument("--pack-format", type=int, default=None, help="Manual Minecraft pack_format number")

    validate_parser = subparsers.add_parser("validate", help="Validate resource pack folder structure")
    validate_parser.add_argument("source", type=Path, help="Resource pack folder to validate")

    formats_parser = subparsers.add_parser("formats", help="Show Minecraft pack format versions")
    help_parser = subparsers.add_parser("help", help="Show command help")

    return parser


def parse_args() -> argparse.Namespace:
    parser = make_parser()
    return parser.parse_args()


def ask_input(prompt: str, default: str | None = None) -> str:
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    answer = input(prompt).strip()
    return answer or (default or "")


def print_pack_format_reference() -> None:
    print("Minecraft pack formats reference:")
    for entry in PACK_FORMAT_REFERENCE:
        if entry["kind"] == "pack_format":
            print(f" - {entry['version']}: pack_format = {entry['value']}")
        else:
            print(f" - {entry['version']}: min_format = {entry['min_format']}, max_format = {entry['max_format']}")


def main() -> int:
    parser = make_parser()
    args = parse_args()
    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "init":
            folder = args.folder
            if folder is None:
                folder_name = ask_input("Введите имя папки для ресурспака / Enter folder name for the resource pack", "my_pack")
                folder = Path(folder_name)
            else:
                # If user gave a simple name (no separators) assume Desktop target for convenience
                s = str(folder)
                if not folder.is_absolute() and ("/" not in s and "\\" not in s):
                    folder = Path.home() / "Desktop" / folder

            name = ask_input("Введите название пака / Enter pack name", args.name)
            description = ask_input("Введите описание пака / Enter pack description", args.description)
            author = ask_input("Введите имя создателя / Enter author name", args.author)

            selected_version = prompt_version_selection(args.version)
            if selected_version["kind"] == "pack_format":
                pack_format = selected_version["value"]
                min_format = None
                max_format = None
            else:
                pack_format = None
                min_format = selected_version.get("min_format")
                max_format = selected_version.get("max_format")

            if args.pack_format is not None:
                pack_format = args.pack_format
                min_format = None
                max_format = None

            create_template(folder, name, description, author, pack_format, min_format=min_format, max_format=max_format)
        elif args.command == "help":
            parser.print_help()
            return 0
        elif args.command == "build":
            pack_format = args.pack_format
            min_format = None
            max_format = None
            if args.version is not None:
                selected_version = resolve_version_entry(args.version)
                if selected_version["kind"] == "pack_format":
                    pack_format = selected_version["value"]
                else:
                    pack_format = None
                    min_format = selected_version.get("min_format")
                    max_format = selected_version.get("max_format")

            build_zip(
                args.source,
                args.output,
                icon=args.icon,
                name=args.name,
                description=args.description,
                author=args.author,
                pack_format=pack_format,
                min_format=min_format,
                max_format=max_format,
            )
        elif args.command == "validate":
            errors = validate_resourcepack_folder(args.source)
            if errors:
                print("Validation failed:")
                for error in errors:
                    print(f" - {error}")
                return 1
            print("Resource pack folder looks good.")
        elif args.command == "formats":
            print_pack_format_reference()
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
