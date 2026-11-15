# Minecraft Resource Pack Builder

![Uploading изображение.png…]()

[![License](https://img.shields.io/github/license/SanguineCruor/resourcepack-creator-for-minecraft)](https://github.com/SanguineCruor/resourcepack-creator-for-minecraft/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
[![Minecraft](https://img.shields.io/badge/Minecraft-1.6.1%20--%201.21.11-green)]()

Lightweight Python command-line utility for creating, validating, and packaging Minecraft resource packs. No external dependencies. Cross-platform. Bilingual interactive prompts (English/Russian).

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Commands](#commands)
  - [init](#init)
  - [build](#build)
  - [validate](#validate)
  - [formats](#formats)
  - [help](#help)
- [pack.mcmeta Generation](#packmcmeta-generation)
- [Supported Versions](#supported-versions)
- [Folder Structure](#folder-structure)
- [Troubleshooting](#troubleshooting)
- [Exit Codes](#exit-codes)
- [License](#license)

## Overview

Minecraft Resource Pack Builder is a single-file Python script that automates routine operations with Minecraft resource packs:

- Generation of a starter pack folder with `pack.mcmeta` and a placeholder `pack.png`.
- Packaging of a pack folder into a ready-to-use `.zip` archive.
- Validation of folder structure and `pack.mcmeta` metadata.
- Interactive selection of the target Minecraft version with automatic `pack_format` resolution.
- Manual override of `pack_format` or `min_format`/`max_format` values.
- Bilingual prompts (English/Russian) selected based on the system locale.

## Requirements

| Requirement | Value |
|---|---|
| Python | 3.10 or newer |
| External dependencies | None (standard library only) |
| Operating systems | Windows, macOS, Linux |

## Installation

Download `resourcepack_builder.py` and run it with Python 3.10+:

```bash
python resourcepack_builder.py --help
```

## Commands

### init

Creates a new resource pack folder with a starter structure.

```bash
python resourcepack_builder.py init my_pack
```

The command prompts for the pack name, description, author, and target Minecraft version (interactive table).

Options:

| Option | Description |
|---|---|
| `--version "<version>"` | Target Minecraft version, e.g. `"1.21.11"` or `"1.20 - 1.20.1"`; a numeric index from the version table is also accepted |
| `--pack-format <N>` | Manual override of the `pack_format` value |
| `--name <string>` | Pack name |
| `--description <string>` | Pack description |
| `--author <string>` | Pack author |

### build

Packages a resource pack folder into a `.zip` archive.

```bash
python resourcepack_builder.py build my_pack -o my_pack.zip
```

Options:

| Option | Description |
|---|---|
| `-o, --output <path>` | Output ZIP file (default: `resourcepack.zip`) |
| `--icon <path>` | Optional pack icon file, stored as `pack.png` |
| `--name <string>` | Pack name when generating `pack.mcmeta` |
| `--description <string>` | Pack description when generating `pack.mcmeta` |
| `--author <string>` | Pack author |
| `--version "<version>"` | Target Minecraft version |
| `--pack-format <N>` | Manual override of the `pack_format` value |

If `pack.mcmeta` is missing in the source folder, it is generated automatically using the provided options and defaults.

### validate

Checks the resource pack folder structure and metadata.

```bash
python resourcepack_builder.py validate my_pack
```

Validation includes:

- Presence of the pack folder.
- Presence and JSON validity of `pack.mcmeta`.
- Presence of `pack_format` or the `min_format`/`max_format` pair in the `pack` section.
- Presence of the `assets/minecraft` folder structure.

### formats

Displays the full reference table of Minecraft versions and corresponding pack format numbers.

```bash
python resourcepack_builder.py formats
```

### help

Displays the general command overview.

```bash
python resourcepack_builder.py help
```

## pack.mcmeta Generation

The tool automatically writes `pack.mcmeta` using one of two styles:

| Style | Applicable versions | Fields |
|---|---|---|
| Legacy | 1.6.1 – 1.21.8 | `pack_format` |
| Modern | 1.21.9 and newer | `min_format`, `max_format` |

The interactive version table selects the appropriate style and values automatically. Manual override is available via `--pack-format`.

## Supported Versions

| Minecraft version(s) | pack_format | Note |
|---|---|---|
| 1.6.1 – 1.8.9 | 1 | |
| 1.9 – 1.10.2 | 2 | |
| 1.11 – 1.12.2 | 3 | |
| 1.13 – 1.14.4 | 4 | |
| 1.15 – 1.16.1 | 5 | |
| 1.16.2 – 1.16.5 | 6 | |
| 1.17 – 1.17.1 | 7 | |
| 1.18 – 1.18.2 | 8 | |
| 1.19 – 1.19.2 | 9 | |
| 1.19.3 | 10 | |
| 1.19.4 | 12 | |
| 1.20 – 1.20.1 | 15 | |
| 1.20.2 | 18 | |
| 1.20.3 – 1.20.4 | 26 | |
| 1.20.5 – 1.20.6 | 32 | |
| 1.21 – 1.21.1 | 34 | |
| 1.21.2 – 1.21.3 | 42 | |
| 1.21.4 | 46 | |
| 1.21.5 | 55 | |
| 1.21.6 | 63 | |
| 1.21.7 – 1.21.8 | 64 | |
| 1.21.9 – 1.21.10 | 88.0 | `min_format` / `max_format` |
| 1.21.11 | 94.1 | `min_format` / `max_format` |

## Folder Structure

```
my_pack/
├── pack.mcmeta          (auto-generated)
├── pack.png             (custom icon, 256x256)
└── assets/minecraft/
    ├── textures/block/     (.png files)
    ├── textures/item/
    ├── sounds/             (.ogg files)
    ├── models/
    ├── font/
    └── lang/
```

## Troubleshooting

| Symptom | Resolution |
|---|---|
| `pack.mcmeta` is reported as invalid | Verify JSON syntax and the presence of the `pack` section with `pack_format` or `min_format`/`max_format` |
| `No assets/minecraft folder structure found` | Create the `assets/minecraft` folder inside the pack |
| Minecraft does not load the pack | Run `validate` and confirm the `pack_format` matches the target game version |

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Error (see the message printed to stderr) |

## License

Distributed under the MIT License.
