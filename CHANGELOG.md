# Changelog

## 0.2.1 — 2026-08-21

- Regenerated model artifacts with sysml2kit 0.3.1's corrected metadata
  quoting (`engine = "phased-array-systems"`, double quotes).
- New `verify` extra installs everything the executable example needs:
  `pip install "sysml2kit-rf-library[verify]"`.
- `docs/verification.md` named a nonexistent `phased-array-systems>=0.14`;
  corrected to `>=0.13`, and the literal output numbers moved behind the
  `pas`-marked test instead of living unverified in prose.
- `scripts/check_parse.py` now asserts text/JSON element-kind parity per
  file, so a parser regression that drops a kind fails CI.

## Unreleased

- SatcomTerminalPAS: an executable verification example whose five
  requirements use metric keys phased-array-systems emits, bound to the
  `phased-array-systems` engine via `verificationBinding`; the study payload
  ships next to the interchange JSON.
- Docs site at https://jman4162.github.io/sysml2kit-rf-library/.

## 0.1.0 — 2026-08-21

- RFVocabulary, RFParts, RFRequirements, RFAnalyses packages.
- SatcomTerminal28GHz worked example mirroring the aedl t3-001 benchmark.
- Python loader (`load_model`, `models_dir`) over committed interchange JSON.
