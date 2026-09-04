#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
OUT = ROOT / "_site"

if OUT.exists():
    shutil.rmtree(OUT)

# Preserve the existing secondary pages and static assets.
shutil.copytree(DOCS, OUT)

# The published site is governed from the repository root.
shutil.copy2(ROOT / "index.html", OUT / "index.html")
if ASSETS.exists():
    shutil.copytree(ASSETS, OUT / "assets", dirs_exist_ok=True)

# Derived machine-readable evidence remains available to the presentation.
shutil.copytree(DATA, OUT / "data")

print(f"Built {OUT} from root index/assets + docs routes + data")
