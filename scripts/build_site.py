#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
OUT = ROOT / "_site"

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(DOCS, OUT)
shutil.copytree(DATA, OUT / "data")
print(f"Built {OUT} from docs/ + data/")
