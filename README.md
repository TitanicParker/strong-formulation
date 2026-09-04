# Strong Formulation

A structured evidential reconstruction of a longitudinal neurological record.

## The central issue

The repository examines a founding documentary synthesis that omitted the patient's direct challenge to an unresolved disposition, and the later use of documentary continuity to justify the historical pathway.

> **The Protest broke the shared understanding. The synthesis removed the break. The later record documented continuity across the gap.**

## How to read it

1. [`founding.md`](founding.md) — the case in plain language.
2. **GitHub Pages case presentation** — the 90-second and 10-minute routes.
3. **Evidence map / source-audit mode** — claim → evidence → consequence with stable `CLIN-` references.
4. [`SRC_COMPLETE_RECORD_FORENSIC.md`](SRC_COMPLETE_RECORD_FORENSIC.md) — canonical longitudinal primary-record transcription.
5. [`ANALYTICAL_RESERVOIR_DEFENDANT_RISK_ORDERED.md`](ANALYTICAL_RESERVOIR_DEFENDANT_RISK_ORDERED.md) — the full 38-profile analytical reservoir.

## What it is not

This repository does not allege that every clinical entry is false. It does not require a single-mechanism explanation for every structural foot finding, and it does not require proof of private motive. Failure to prove proposition X is not affirmative proof of the opposite proposition.

## Source architecture

- **FOUNDING** = the case in human language.
- **RESERVOIR** = the analytical hierarchy.
- **FORENSIC RECORD** = the evidential substrate.
- **`data/`** = machine-readable derived claims, events, evidence and profile metadata.
- **`docs/`** = privacy-minimised public presentation built from those derived layers.

The three canonical source files remain untouched.

## Status

Analytical / counsel preparation; source-backed and continuously auditable. The Pages presentation deliberately excludes unnecessary personal identifiers even where those identifiers already exist in the public canonical record.

## Build and validation

```bash
python scripts/validate.py
python scripts/build_site.py
```

The Pages workflow publishes only the generated `_site/` directory: presentation files plus derived data. It does **not** publish the canonical forensic source as part of the site artifact.
