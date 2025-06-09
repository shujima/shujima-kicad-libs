#!/usr/bin/env python3
import os
import re
from pathlib import Path

README_PATH = Path("README.md")
SYM_PATH = Path("symbols")
MOD_PATH = Path("footprints")

def extract_symbol_names(sym_file):
    content = sym_file.read_text(encoding="utf-8")
    return re.findall(r"\(symbol\s+([^\s]+)", content)

def extract_footprint_names(mod_file):
    content = mod_file.read_text(encoding="utf-8")
    return re.findall(r"\(module\s+([^\s]+)", content)

def scan_components():
    symbols = []
    if SYM_PATH.exists():
        for sym in SYM_PATH.glob("*.kicad_sym"):
            symbols.extend(extract_symbol_names(sym))

    footprints = []
    if MOD_PATH.exists():
        for moddir in MOD_PATH.iterdir():
            for mod in moddir.glob("*.kicad_mod"):
                footprints.extend(extract_footprint_names(mod))

    return sorted(set(symbols)), sorted(set(footprints))

def update_readme(symbols, footprints):
    if not README_PATH.exists():
        readme = ""
    else:
        readme = README_PATH.read_text(encoding="utf-8")

    new_section = "## コンポーネント一覧\n\n"
    if symbols:
        new_section += "### シンボル\n" + "\n".join(f"- `{s}`" for s in symbols) + "\n\n"
    if footprints:
        new_section += "### フットプリント\n" + "\n".join(f"- `{f}`" for f in footprints) + "\n"

    # セクションを置き換え
    updated = re.sub(
        r"<!-- BEGIN:liblist -->.*<!-- END:liblist -->",
        f"<!-- BEGIN:liblist -->\n{new_section}<!-- END:liblist -->",
        readme,
        flags=re.DOTALL,
    )

    README_PATH.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    syms, mods = scan_components()
    update_readme(syms, mods)

