#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
FORENSIC = ROOT / "SRC_COMPLETE_RECORD_FORENSIC.md"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return []


def norm(text: str) -> str:
    """Normalize canonical transcription text for locked-quote comparison.

    The forensic source prefixes every physical line with a stable CLIN identifier.
    Those provenance markers can fall inside a sentence when a quote spans lines,
    so they must not participate in literal quote matching.
    """
    text = re.sub(r"\bCLIN-\d{6}\b", " ", text)
    return re.sub(r"\s+", " ", text).strip()


evidence = load_json(DATA / "evidence-index.json")
claims = load_json(DATA / "claims.json")
timeline = load_json(DATA / "timeline.json")
profiles = load_json(DATA / "profiles.json")
knowledge = load_json(DATA / "knowledge-state.json")

source = FORENSIC.read_text(encoding="utf-8", errors="replace") if FORENSIC.exists() else ""
source_norm = norm(source)
clin_ids = set(re.findall(r"CLIN-\d{6}", source))

for item in evidence:
    for key in ("clin_start", "clin_end"):
        cid = item.get(key)
        if cid and cid not in clin_ids:
            fail(f"{item.get('id')}: missing {key} {cid} in canonical forensic record")
    try:
        if int(item["clin_start"].split("-")[1]) > int(item["clin_end"].split("-")[1]):
            fail(f"{item['id']}: CLIN range is reversed")
    except Exception:
        fail(f"{item.get('id')}: malformed CLIN range")
    if item.get("quote_check") and item.get("quote") and norm(item["quote"]) not in source_norm:
        fail(f"{item['id']}: locked quote no longer matches canonical source")

profile_ids = {p.get("id") for p in profiles}
evidence_ids = {e.get("id") for e in evidence}
claim_ids = {c.get("id") for c in claims}

for c in claims:
    for eid in c.get("evidence", []):
        if eid not in evidence_ids:
            fail(f"{c['id']}: unknown evidence {eid}")
    for pid in c.get("profiles", []):
        if pid not in profile_ids:
            fail(f"{c['id']}: unknown profile {pid}")
    for dep in c.get("dependencies", []):
        if dep not in claim_ids:
            fail(f"{c['id']}: unknown dependency {dep}")

for e in evidence:
    for pid in e.get("profiles", []):
        if pid not in profile_ids:
            fail(f"{e['id']}: unknown profile {pid}")

iso_re = re.compile(r"^\d{4}(?:-\d{2}(?:-\d{2})?)?$")
for collection_name, collection in (("timeline", timeline), ("evidence", evidence), ("knowledge-state", knowledge)):
    for item in collection:
        date = item.get("date")
        if date and not iso_re.match(date):
            fail(f"{collection_name} {item.get('id', '')}: non-ISO date {date}")

# Scan all derived files for CLIN references and ensure they exist.
for folder in (DATA, DOCS):
    if not folder.exists():
        continue
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".html", ".js", ".css", ".svg", ".md"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for cid in re.findall(r"CLIN-\d{6}", text):
                if cid not in clin_ids:
                    fail(f"{path.relative_to(ROOT)} references missing {cid}")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag in {"a", "link", "script", "img"}:
            d = dict(attrs)
            for key in ("href", "src"):
                if d.get(key):
                    self.links.append(d[key])

for html in DOCS.glob("*.html"):
    parser = LinkParser()
    parser.feed(html.read_text(encoding="utf-8"))
    for link in parser.links:
        if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        target = link.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        candidate = (html.parent / target).resolve()
        if target.startswith("data/"):
            candidate = (DATA / target.removeprefix("data/")).resolve()
        if not candidate.exists():
            fail(f"{html.relative_to(ROOT)}: unresolved internal link {link}")

# Presentation privacy guardrails. Canonical sources are intentionally excluded.
privacy_patterns = {
    "DOB-like date": re.compile(r"\b\d{2}/\d{2}/\d{4}\b"),
    "Irish mobile-like number": re.compile(r"\b08\d{8}\b"),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
}
for folder in (DATA, DOCS):
    if not folder.exists():
        continue
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".html", ".js", ".css", ".svg", ".md"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in privacy_patterns.items():
                if pattern.search(text):
                    fail(f"{path.relative_to(ROOT)}: privacy scanner found {label}")

if errors:
    print("VALIDATION FAILED")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print(f"Validation passed: {len(evidence)} evidence items, {len(claims)} claims, {len(profiles)} profiles, {len(timeline)} timeline events.")
