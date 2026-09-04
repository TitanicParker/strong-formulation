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

# Publish a single stylesheet used by every route. The phone-first refinement
# layer is appended after the core design so mobile rules consistently win,
# including on the older secondary pages in docs/.
core_css = ASSETS / "styles.css"
mobile_css = ASSETS / "mobile.css"
published_css = OUT / "assets" / "styles.css"
if core_css.exists():
    css = core_css.read_text(encoding="utf-8")
    if mobile_css.exists():
        css += "\n\n" + mobile_css.read_text(encoding="utf-8")
    published_css.write_text(css, encoding="utf-8")

# Derived machine-readable evidence remains available to the presentation.
shutil.copytree(DATA, OUT / "data")

print(f"Built {OUT} from root index/assets + docs routes + data")
