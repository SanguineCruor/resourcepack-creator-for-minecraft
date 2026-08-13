Minecraft Resource Pack Builder
MIT Licensed – freely use, modify, and distribute.
![License](https://img.shields.io/github/license/SanguineCruor/resourcepack-creator-for-minecraft)

Lightweight Python CLI for creating, validating, and packaging Minecraft resource packs (1.6.1 – 1.21.11).
No external dependencies, cross‑platform (Windows/macOS/Linux), bilingual prompts (en/ru).

Features
✅ Generate starter folder with pack.mcmeta and pack.png

✅ Build ready‑to‑use .zip archives

✅ Validate folder structure and metadata

✅ Interactive version selection (English/Russian)

✅ Manual override for pack_format or min/max_format

✅ Bilingual prompts (en/ru) based on system locale

Installation
Download resourcepack_builder.py and run with Python 3.10+:

bash
python resourcepack_builder.py --help
Commands (Quick Start)
init – create a new pack
bash
python resourcepack_builder.py init my_pack
Prompts for name, description, author, and Minecraft version (interactive table).
Options:

--version "1.21.11" or --version 23 (by number)

--pack-format 94 (manual override)

--name, --description, --author

build – package into .zip
bash
python resourcepack_builder.py build my_pack -o my_pack.zip
Options:

--icon icon.png

--name, --description, --author

--version "1.20.5" or --pack-format 55

validate – check structure
bash
python resourcepack_builder.py validate my_pack
Checks folder, pack.mcmeta (valid JSON + format fields), and assets/minecraft subfolders.

formats – show version table
bash
python resourcepack_builder.py formats
Displays all pack_format numbers and ranges.

help – show this overview
bash
python resourcepack_builder.py help
pack.mcmeta generation
Automatically writes:

Old style: pack_format: N

New style (1.21.9+): min_format / max_format

The interactive table picks the right format for you.

Supported versions (simplified)
MC Version(s)	pack_format	Note
1.6.1 – 1.8.9	1	
1.9 – 1.10.2	2	
1.11 – 1.12.2	3	
1.13 – 1.14.4	4	
1.15 – 1.16.1	5	
1.16.2 – 1.16.5	6	
1.17 – 1.17.1	7	
1.18 – 1.18.2	8	
1.19 – 1.19.2	9	
1.19.3	10	
1.19.4	12	
1.20 – 1.20.1	15	
1.20.2	18	
1.20.3 – 1.20.4	26	
1.20.5 – 1.20.6	32	
1.21 – 1.21.1	34	
1.21.2 – 1.21.3	42	
1.21.4	46	
1.21.5	55	
1.21.6	63	
1.21.7 – 1.21.8	64	
1.21.9 – 1.21.10	88.0 *	min/max_format
1.21.11	94.1 *	min/max_format
Folder structure
text
my_pack/
├── pack.mcmeta          (auto‑generated)
├── pack.png             (custom icon 256×256)
└── assets/minecraft/
    ├── textures/block/     (your .png)
    ├── textures/item/
    ├── sounds/             (.ogg)
    ├── models/
    ├── font/
    └── lang/
Troubleshooting (common)
pack.mcmeta invalid → check JSON syntax and pack + author keys.

No assets/minecraft → create that folder inside your pack.

Minecraft doesn't load pack → run validate, ensure correct pack_format.

Exit codes: 0 = success, 1 = error (see message).

Requirements & License
Python 3.10+ (standard library only)

MIT License – see LICENSE file.

Happy pack building!
