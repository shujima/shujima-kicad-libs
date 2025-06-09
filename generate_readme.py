#!/usr/bin/env python3
import os
import re
from pathlib import Path

README_PATH = Path("README.md")
REPO_ROOT = Path(".")

def extract_symbol_names(sym_file: Path):
    content = sym_file.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r"\(symbol\s+([^\s\)]+)", content)

def extract_footprint_names(mod_file: Path):
    content = mod_file.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r'\((?:module|footprint)\s+"?([^\s\)"]+)"?', content)


def scan_components():
    symbols = []
    footprints = []

    for path in REPO_ROOT.rglob("*.kicad_sym"):
        symbols.extend(extract_symbol_names(path))

    for path in REPO_ROOT.rglob("*.kicad_mod"):
        footprints.extend(extract_footprint_names(path))

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

    updated = re.sub(
        r"<!-- BEGIN:liblist -->.*<!-- END:liblist -->",
        f"<!-- BEGIN:liblist -->\n{new_section}<!-- END:liblist -->",
        readme,
        flags=re.DOTALL,
    )

    README_PATH.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    syms, mods = scan_components()
    print(f"🔍 Found {len(syms)} symbols and {len(mods)} footprints.")
    update_readme(syms, mods)

